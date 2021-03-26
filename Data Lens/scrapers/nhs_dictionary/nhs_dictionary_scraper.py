import json
import logging
import sys
from datetime import datetime

import requests
from bs4 import BeautifulSoup

# Credentials passed in as arguments from the nifi processor
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from requests.adapters import HTTPAdapter, Retry

import entities

elastic_username = sys.argv[1:][0]
elastic_password = sys.argv[2:][0]
elastic_index = sys.argv[3:][0]

es = Elasticsearch([f'https://{elastic_username}:{elastic_password}@elastic.datalens.naimuri.dev:9200'])

today = datetime.now().date()
logging.FileHandler('logs/%s.log' % today, mode='a', encoding=None, delay=False)
logging.basicConfig(filename='logs/%s.log' % today, level=logging.INFO, format="%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")


logging.info("starting scraping " + datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3])


def get_vectors(data):
    retry_strategy = Retry(
        total=3,
        status_forcelist=[429, 500, 502, 503, 504],
        method_whitelist=["HEAD", "GET", "OPTIONS"]
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
        return eval(r.text) if isinstance(eval(r.text), str) else None
    except requests.HTTPError as exception:
        logging.error(exception)


def get_entities(data, fields):
    str_ = ""

    for field in fields:
        if field in data:
            str_ += data[field] + " "

    return {k: v for k, v in entities.entities(str_).items() if v}


def get_page(url):
    try:
        response = requests.get(url)
        # response.raise_for_status()
        return response
    except requests.HTTPError as exception:
        logging.error(exception)


def send_to_elastic(result_object):
    try:
        es.index(index=elastic_index, doc_type='_doc', body=json.dumps(result_object, ensure_ascii=False))
    except AttributeError as ex:
        logging.error(ex)


topics = ["nhs_business_definitions_overview.html", "supporting_information_overview.html", "classes_overview.html",
          "attributes_overview.html", "data_elements_overview.html"]

base_uri = "https://datadictionary.nhs.uk/"

for topic in topics:
    results_request = get_page(base_uri + topic)
    if results_request.status_code == 200:
        results = BeautifulSoup(results_request.text, "html.parser")

        result_topics = results.select("td > a")
        elastic_batch = []

        if len(result_topics) > 0:
            for item in result_topics:
                record = dict()

                item_page_request = get_page(base_uri + item['href'])

                if item_page_request.status_code == 200:
                    item_page = BeautifulSoup(item_page_request.text, "html.parser")

                    record['title'] = item_page.find("meta", {"name": "name"})['content']
                    record['description'] = item_page.find("meta", {"name": "description"})['content']
                    record['type'] = item_page.find("meta", {"name": "stereotype"})['content']
                    record['url'] = base_uri + item_page.find("meta", {"name": "wh-out-relpath"})['content']
                    record['source'] = "NHS Data Dictionary"
                    record['source_url'] = base_uri + topic
                    record["ingest.timestamp"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]

                    # used to grab additional information for data dict such as plural and context terms.
                    identifier = item_page.find("meta", {"name": "DC.identifier"})['content']
                    if identifier:
                        plural_and_context_table = item_page.find("article",
                                                                  {"id": identifier + ".also_known_as"}).select(
                            "tbody > tr") if item_page.find("article", {"id": identifier + ".also_known_as"}) else None

                        if plural_and_context_table:
                            for row in plural_and_context_table:
                                cells = row.findAll("td")
                                record[cells[0].getText().lower().replace(" ", "_")] = cells[1].getText()

                        # Find and store entities.
                        entities_ = get_entities(record, ["description", "title"])
                        if entities_:
                            record["entities"] = entities_

                        vectors = get_vectors(record)
                        if vectors:
                            record['text_vector'] = json.loads(vectors)

                    elastic_batch.append(record)

                    if len(elastic_batch) == 100:
                        # Send the search result to elastic search and clear the list
                        bulk(es, elastic_batch, index=elastic_index)
                        elastic_batch.clear()
                else:
                    continue

            bulk(es, elastic_batch, index=elastic_index)
    else:
        continue

logging.info("Finished Scraping")