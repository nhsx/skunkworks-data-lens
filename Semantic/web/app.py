import certifi, html2text, json, nltk, os, string

from elasticsearch import Elasticsearch, helpers
from elasticsearch.helpers import bulk, scan
from flask import Blueprint, Flask, jsonify, render_template, request
from flask_restplus import Api, fields, inputs, reqparse, Resource
from numpy import array, dot, mean
from numpy.linalg import norm
from scipy.stats import zscore
from urllib.parse import unquote

from embedding import BiobertEmbedding, SPLITTER

# Environment variables
ELASTICSEARCH_ADDRESS = os.environ['ELASTICSEARCH_ADDRESS']
SEARCH_SIZE = os.environ['DATALENS_SEARCH_SIZE']
MINIMUM_ZSCORE = float(os.environ['DATALENS_MINIMUM_ZSCORE'])
ELASTICSEARCH_USERNAME = os.environ['ELASTICSEARCH_USERNAME']
ELASTICSEARCH_PASSWORD = os.environ['ELASTICSEARCH_PASSWORD']

# Other static variables
MODEL_NAME = 'model'
WORD_LIMIT = 500
SOURCES_FILE = 'config/sources.json'

# Create the app
app = Flask(__name__)
api = Api(app)
name_space = api.namespace('semantic', description='Data Lens Semantic Search')
print("App started")
        
# Load BioBERT model
print("Loading model")
bc = BiobertEmbedding(MODEL_NAME)

# Start elastic client
client = Elasticsearch(
    ELASTICSEARCH_ADDRESS,
    http_auth=(ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD),
    use_ssl=True,
    verify_certs=True,
    ca_certs=certifi.where()
)

# Instantiate HTML converter
html_converter = html2text.HTML2Text()
html_converter.ignore_links = True


@name_space.route('/embed-by-id')
class EmbedById(Resource):
    
    @api.doc(params={
        'source': 'A dataset source',
        'id': 'A document ID'
    })
    def post(self):

        # Parse inputs
        source_name = request.args.get('source', None)
        id = request.args.get('id', None)
        if source_name is None or id is None:
            return
        
        # Load source
        source = get_source_config(source_name)
        if source is None:
            api.abort(400)
                
        # Get document by id
        document = client.get(index=my_source["readIndex"], id=id)
        
        # Vectorise
        searchable_text = extract_searchable_text(document, source["searchableFields"])
        vector = bc.sentence_vector(searchable_text)
        if vector is None:
            return
        
        # Store
        script_query = {
            "query": {
                "bool": {
                    "filter": {
                        "term": {"_id": id}
                    }
                }
            },
            "script": {
                "source": "ctx._source.text_vector=" + str(vector.numpy().tolist()),
                "lang": "painless"
            }
        }
        client.update_by_query(index=my_source["writeIndex"], body=script_query)


@name_space.route('/embed')
class Embedder(Resource):
    
    resource_fields = api.model('Resource', {
        'body': fields.String,
    })
    
    @api.doc(
        params={'target': 'An NHSx datasource'},
        body=resource_fields,
        responses={400: 'Bad Request',
                   424: 'Failed Dependency'}
    )
    def post(self):
        
        document = request.json
        target = request.args.get('target', None)
        
        source = get_source_config(target)
        if source is None:
            api.abort(400)

        text_vector = None
        try:
            searchable_text = extract_searchable_text(document, source["searchableFields"])
        except:
            print('Searchable text could not be extracted from document body: ' + document)
            api.abort(500)

        if len(searchable_text) == 0:
            api.abort(400)
            
        text_vector = bc.sentence_vector(searchable_text)
        if text_vector is None:
            api.abort(424)
        
        return str(text_vector.numpy().tolist())
    

    @api.doc(params={'target': 'An NHSx datasource'})
    def put(self):
        
        # TODO: Make this a real put that adds the job onto a retry queue
        
        target = request.args.get('target', None)
        
        # Get information about the elastic sources
        embedded = []
        with open(SOURCES_FILE) as afile:
            sources = json.load(afile)
            
            # Process each source in turn
            for source in sources.values():
                
                # Allow one source at a time
                if target is not None and source['source'] != target:
                    continue
        
                # Get all documents from the READ index
                documents = scan(
                    client,
                    index=source["readIndex"],
                    query={"query": {"match_all": {}}}
                )
                
                # Embed the text vector for each document
                updated_docs = []
                for document in list(documents):
                    
                    print("Embedding text vector in document ID", document["_id"])
                    text_vector = None
                    
                    # Calculate the text vector
                    try:
                        searchable_text = extract_searchable_text(document["_source"], source["searchableFields"])
                    except:
                        print('Searchable text could not be extracted from document body: ' + document)
                        continue
                    if len(searchable_text) > 0:
                        text_vector = bc.sentence_vector(searchable_text)
                        if text_vector is None:
                            remove_text_vector(client, source["writeIndex"], document["_id"])
                            continue
                        document["_source"]["text_vector"] = text_vector.numpy().tolist()
                        updated_docs.append({
                            "_index": source["writeIndex"],
                            "_id": document["_id"],
                            "_type": document["_type"],
                            "_source": document["_source"]
                        })

                    if len(updated_docs) >= 50:
                        print("Updating elastic")
                        helpers.bulk(client, updated_docs)
                        updated_docs = []

                if len(updated_docs) > 0:
                    helpers.bulk(client, updated_docs)


@name_space.route('/search')
class SemanticSearch(Resource):
    
    @api.doc(params={'query': 'A user query'})
    def get(self):

        # Getting and vectorising query
        query = request.args.get('query')
        results = search(query)
        if results is None:
            return []
        
        return jsonify(results)
    
    
@name_space.route('/search-and-filter')
class SemanticSearchAndFilter(Resource):
    
    @api.doc(params={'query': 'A user query'},
             responses={404: 'Not Found'}
    )
    def get(self):

        query = request.args.get('query')
        unfiltered_results = search(query)
        if unfiltered_results is None:
            api.abort(404)
        scored_results = calculate_z_scores(unfiltered_results)
        
        return jsonify([result for result in scored_results if result["_zscore"] > MINIMUM_ZSCORE])


@name_space.route('/recommendations')
class SemanticRecommendations(Resource):

    @api.doc(params={
        'index': 'A source index',
        'ID': 'A document ID'
    })
    def get(self):
        index = request.args.get('index', None)
        doc_id = request.args.get('ID', None)

        # Get document by the index and ID
        document = client.get(index=index, id=doc_id)

        # Extract text_vector
        text_vector = document["_source"]['text_vectors']

        # Setting up the search script
        search_script = {
            "script_score": {
                "query": {"exists": {"field": "text_vectors"}},
                "script": {
                    "source": "cosineSimilarity(params.textVector, doc['text_vectors']) + 1.0",
                    "params": {"textVector": text_vector}
                }
            }
        }

        # Creating empty lists to add indices and searchable fields to, from config
        indices = []
        searchable_fields = []
        with open(SOURCES_FILE) as afile:
            sources = json.load(afile)
            for source in sources.values():
                indices.append(source["readIndex"])
            for source in sources.values():
                searchable_fields.append(source["searchableFields"])

        # Flattening list of lists to one list.
        searchable_fields = [y for x in searchable_fields for y in x]

        # Querying elastic from config
        response = client.search(
            index=indices,
            body={
                "size": SEARCH_SIZE,
                "query": search_script
            }
        )

        # Do not return first doc as it matches the same doc that was input
        response = response['hits']['hits'][1:len(response['hits']['hits'])]
        response = calculate_z_scores(response)
        
        return jsonify([result for result in response if result["_zscore"] > MINIMUM_ZSCORE])


def search(query):
    
    query_vector = bc.sentence_vector(query).numpy().tolist()
    if query_vector is None:
        return []
    
    # Setting up the search script
    search_script = {
        "script_score": {
            "query": {"exists": {"field": "text_vectors"}},
            "script": {
                "source": "cosineSimilarity(params.query_vector, doc['text_vectors']) + 1.0",
                "params": {"query_vector": query_vector}
            }
        }
    }

    # Get information about elastic sources
    with open(SOURCES_FILE) as afile:
        sources = json.load(afile)
        
        # Get the list of configured elastic indices
        indices = [ds['readIndex'] for ds in sources.values()]
        searchable_fields = set()
        for source in sources.values():
            for field in source['searchableFields']:
                searchable_fields.add(field)

        # Querying elastic from config
        response = client.search(
            index=indices,
            body={
                "size": SEARCH_SIZE,
                "query": search_script
            }
        )
        
    return response['hits']['hits']


def remove_text_vector(client, index, document_id):
    
    script_query = {
        "query": {
            "bool": {
                "filter": {
                    "term": {"_id": document_id}
                }
            }
        },
        "script": {
            "source": "ctx._source.remove(\"text_vectors\")",
            "lang": "painless"
        }
    }
    client.update_by_query(index=index, body=script_query)
        

def extract_searchable_text(doc, searchable_fields):
    searchable_text = []
    for field in searchable_fields:
        current = doc
        for field_key in field.split("."):
            if current:
                current = current.get(field_key, "")
        if isinstance(current, str):
            searchable_text.append(current)
        elif isinstance(current, list) and len(current) > 0:
            if isinstance(current[0], str):
                searchable_text += current
    if len(searchable_text) == 0:
        return None
    searchable_text = html_converter.handle(" ".join(searchable_text))
    truncated_text = ""
    sentences = SPLITTER.tokenize(searchable_text)
    for sentence in sentences:
        truncated_text += " " + sentence
        if len(truncated_text.split()) > WORD_LIMIT:
            return truncated_text
    return truncated_text.strip()


def get_source_config(source_name):
    
    with open(SOURCES_FILE) as afile:
        sources = json.load(afile)
        for source in sources.values():
            if source["source"] == source_name:
                return source

    return None


def calculate_z_scores(results):
    
    doc_ids = array([doc["_id"] for doc in results])
    scores = array([doc["_score"] for doc in results])
    zscores = zscore(scores)
    zdict = dict(zip(doc_ids, zscores))
    
    for result in results:
        result["_zscore"] = zdict[result["_id"]]
    
    return results


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
