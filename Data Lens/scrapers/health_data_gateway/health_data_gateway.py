import json
import re
import sys
from datetime import datetime
import dateutil.parser
import requests
from dateutil.parser import parse
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from requests.adapters import HTTPAdapter, Retry
import logging

import entities

today = datetime.now().date()
logging.FileHandler('logs/%s.log' % today, mode='a', encoding=None, delay=False)
logging.basicConfig(filename='logs/%s.log' % today, level=logging.INFO,
                    format="%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")


def call_api(offset):
    try:
        response = requests.get("https://api.www.healthdatagateway.org/api/v1/datasets/?limit=100&offset=%s" % offset)
        response.raise_for_status()
        return response
    except requests.HTTPError as exception:
        logging.error(exception.response.text)


def remove_empty_elements(d):
    """recursively remove empty lists, empty dicts, or None elements from a dictionary"""

    def empty(x):
        return x is None or x == {} or x == [] or x == ""

    # Align dates up if the value looks like a date.
    def format_dates(x):
        if isinstance(x, str) and re.fullmatch("[[0-9]*([/-])[0-9]*([/-])[0-9]*", x):

            try:
                return str(dateutil.parser.parse(x))
            except ValueError:
                logging.error("couldnt parse date value: " + x)
                return x
        return x

    if not isinstance(d, (dict, list)):
        return format_dates(d)
    elif isinstance(d, list):
        return [v for v in (remove_empty_elements(v) for v in d) if not empty(v)]
    else:
        return {k: v for k, v in ((k, remove_empty_elements(v)) for k, v in d.items()) if not empty(v)}


def is_date(date_, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        parse(date_, fuzzy=fuzzy)
        return True
    except ValueError:
        return False


def get_vectors(data):
    retry_strategy = Retry(
        total=3,
        status_forcelist=[429, 500, 502, 503, 504],
        method_whitelist=["HEAD", "POST", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)
    headers = {'content-type': 'application/json', "accept": "application/json"}
    source = data['source'].replace(" ", "%20")
    semantic_url = 'http://datalens-semantic-alb-967737509.eu-west-2.elb.amazonaws.com/semantic/embed?target=' + source

    if "description" in data and isinstance(data["description"], list):
        data["description"] = ' '.join(data["description"])

    try:
        r = http.post(semantic_url, data=json.dumps(data), headers=headers)
        r.raise_for_status()
        return eval(r.text) if isinstance(eval(r.text), str) else None
    except requests.HTTPError as exception:
        logging.error(exception.response.text)


def get_entities(data, fields):
    str_ = ""

    for field in fields:
        if field in data:
            str_ += data[field] + " "

    return {k: v for k, v in entities.entities(str_).items() if v}


titles = []
elastic_batch = []
offset_number = 0

# Credentials passed in as arguments from the nifi processor
elastic_username = sys.argv[1:][0]
elastic_password = sys.argv[2:][0]
elastic_index = sys.argv[3:][0]

keep_calling = True
es = Elasticsearch([f'https://{elastic_username}:{elastic_password}@elastic.datalens.naimuri.dev:9200'])

logging.info("Scraping started:")

while keep_calling:
    results = call_api(offset_number)
    results_as_json = json.loads(results.text)

    if len(results_as_json["data"]) > 0:

        for item in results_as_json["data"]:

            # API is annoying and returns duplicate data. To stop this I am storing the titles in a list and then checking each new item to see if I have seen it before.
            if item["name"] in titles:
                logging.info("we have seen this title before: " + item['name'] + " I am skipping this one")
            else:
                titles.append(item["name"])

                # Rename _id as this is reserved for elastic although we will be using this ID for elasitc
                elastic_id = item["_id"]
                del item["_id"]

                record = remove_empty_elements(item)

                if "datasetfields" in record:

                    # Copy items in the meta data section to the top level.
                    if "metadataschema" in record["datasetfields"]:
                        if "description" in record["datasetfields"]["metadataschema"]:
                            record["description"] = record["datasetfields"]["metadataschema"]["description"]
                        if "url" in record["datasetfields"]["metadataschema"]:
                            record["url"] = record["datasetfields"]["metadataschema"]["url"]

                    if "datasetEndDate" in record["datasetfields"] and not is_date(
                            record["datasetfields"]["datasetEndDate"]):
                        del record['datasetfields']['datasetEndDate']

                    if "datasetStartDate" in record["datasetfields"] and not is_date(
                            record["datasetfields"]["datasetStartDate"]):
                        del record['datasetfields']['datasetStartDate']

                    if "releaseDate" in record["datasetfields"] and not is_date(record["datasetfields"]["releaseDate"]):
                        del record['datasetfields']['releaseDate']

                # Add common data
                record["ingest.timestamp"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
                record["title"] = record["name"]
                record["source"] = "Health Data Innovation Gateway"
                record["source_url"] = "https://healthdatagateway.org"
                record["type"] = "Dataset"

                # Find and store entities.
                entities_ = get_entities(record, ["title", "introduction", "description"])
                if entities_:
                    record["entities"] = entities_
                vectors = get_vectors(record)
                if vectors:
                    record['text_vector'] = json.loads(vectors)

                logging.info(record['title'])

                # Send item to elastic
                elastic_batch.append(record)

            if len(elastic_batch) == 100:
                # Send the search result to elastic search and clear the list
                bulk(es, elastic_batch, index=elastic_index)
                elastic_batch.clear()

        offset_number += 101
    else:
        logging.info("Scraping finished")
        keep_calling = False
        bulk(es, elastic_batch, index=elastic_index)
        elastic_batch.clear()
