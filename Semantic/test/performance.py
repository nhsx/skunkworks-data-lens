import requests
import pandas as pd
from urllib.parse import quote
from elasticsearch import Elasticsearch
import certifi
import numpy as np


# Declare the location of queries and where to write the results to.
QUERIES_FILE_PATH = '/queries.csv'
RESULTS_WRITE_FILE_PATH = '/Users/alex.vandenbos/code/PERFORMANCE.csv'
ELASTICSEARCH_ADDRESS = 'https://elastic.datalens.naimuri.dev:9200'

cols = [0]
queries = pd.read_csv(QUERIES_FILE_PATH)
semanticResults = pd.DataFrame(range(1, 500), columns=['semanticResults'])
keywordResults = pd.DataFrame(range(1, 500), columns=['keywordResults'])

# Top 10 results for each query for SEMANTIC SEARCH
for n in range(0, (len(queries[queries.columns[0]]))):
    QUERY = queries[queries.columns[0]][n]
    QUERY_SQL = quote(QUERY)

    # Send request and query to search and filter endpoint on API.
    r = requests.get('http://127.0.0.1:5000/semantic/search-and-filter?query=' + QUERY_SQL)
    results = r.json()

    # Define id list to be populated with id's of top results.
    idList = []

    # Remove unneeded keys from results - keeps id.
    for i in range(len(results)):
        del results[i]['_source']
        del results[i]['_index']
        del results[i]['_type']
        idList.append(results[i]['_id'])

    # Prepare results to be added to a dataframe.
    ids = pd.DataFrame(idList, columns=[QUERY + ' id SS'])
    semanticResults = pd.concat([semanticResults, ids], axis=1)


# Top 10 results for each query for KEYWORD SEARCH.
idList = []
for n in range(0, (len(queries[queries.columns[0]]))):
    QUERY = queries[queries.columns[0]][n]

    # Create elastic client to allow script to query elastic
    client = Elasticsearch(
        ELASTICSEARCH_ADDRESS,
        http_auth=('elastic', 'com205'),
        use_ssl=True,
        verify_certs=True,
        ca_certs=certifi.where()
    )

    # Query elastic client with the same query used by the UI
    documents = client.search(index=("com205-fingertips", "com205-nhs-digital", "com205-nhs-england-databases",
                                     "com205-nhs-england-data-catalogue"),
                              size=10000,
                              body={
                                    "query": {
                                        "bool": {
                                            "should": [
                                                {
                                                    "query_string": {
                                                        "query": QUERY,
                                                        "type": "best_fields",
                                                        "phrase_slop": 0,
                                                        "default_operator": "AND",
                                                        "fields": [
                                                            "title^5",
                                                            "*"
                                                        ],
                                                        "analyze_wildcard": True,
                                                        "boost": 2
                                                    }
                                                },
                                                {
                                                    "query_string": {
                                                        "query": QUERY,
                                                        "type": "best_fields",
                                                        "default_operator": "AND",
                                                        "fields": [
                                                            "title^5",
                                                            "*"
                                                        ],
                                                        "analyze_wildcard": True,
                                                        "boost": 1.5
                                                    }
                                                },
                                                {
                                                    "query_string": {
                                                        "query": QUERY,
                                                        "type": "cross_fields",
                                                        "default_operator": "OR",
                                                        "minimum_should_match": "3<90%",
                                                        "fields": [
                                                            "title^2",
                                                            "*"
                                                        ],
                                                        "analyze_wildcard":True,
                                                        "boost": 1
                                                    }
                                                },
                                                {
                                                    "query_string": {
                                                        "query": QUERY,
                                                        "type": "cross_fields",
                                                        "minimum_should_match": "50%",
                                                        "default_operator": "OR",
                                                        "fields": [
                                                            "title^2",
                                                            "*"
                                                        ],
                                                        "analyze_wildcard": True,
                                                        "boost": 0.01
                                                    }
                                                }
                                            ]
                                        }
                                    }
    })

    # Record result id's
    idList = [doc["_id"] for doc in documents['hits']['hits']]
    idList = pd.DataFrame(idList, columns=[QUERY + ' id KS'])
    keywordResults = pd.concat([keywordResults, idList], axis=1)


# Combine semantic search results and keyword search results
results = pd.concat([semanticResults, keywordResults], axis=1)
del results['semanticResults']
del results['keywordResults']


# Finds the proportion of semantic search results which are also present in keyword search results
# Create dataframe with relevant columns
matchingResults = pd.DataFrame(queries)
matchingResults['Length KS'] = None
matchingResults['Length SS'] = None
matchingResults['Matching'] = None
matchingResults['Proportion of SS in KS'] = None

# Populate columns for each query
for n in range(0, (len(queries[queries.columns[0]]))):
    QUERY = queries[queries.columns[0]][n]

    keywordSearch = set(results[QUERY + ' id KS'])
    keywordSearch.discard(np.nan)
    semanticSearch = set(results[QUERY + ' id SS'])
    semanticSearch.discard(np.nan)
    matches = keywordSearch.intersection(semanticSearch)
    proportion = (str(round((len(matches)/len(semanticSearch))*100, 2))) + '%'

    matchingResults['Length KS'][n] = len(keywordSearch)
    matchingResults['Length SS'][n] = len(semanticSearch)
    matchingResults['Matching'][n] = len(matches)
    matchingResults['Proportion of SS in KS'][n] = proportion

# Print out final results and write to a csv file in your chosen path
print(matchingResults)
matchingResults.to_csv(RESULTS_WRITE_FILE_PATH)
