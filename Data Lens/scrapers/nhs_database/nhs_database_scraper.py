import json
import logging
import sys
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from requests.adapters import HTTPAdapter, Retry

import entities


def get_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response
    except requests.HTTPError as exception:
        logging.error(exception)


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



# Credentials passed in as arguments from the nifi processor
elastic_username = sys.argv[1:][0]
elastic_password = sys.argv[2:][0]
elastic_index = sys.argv[3:][0]


today = datetime.now().date()
logging.FileHandler('logs/%s.log' % today, mode='a', encoding=None, delay=False)
logging.basicConfig(filename='logs/%s.log' % today, level=logging.INFO, format="%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")


logging.info("starting scraping " + datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3])

database_list_get = get_page("https://data.england.nhs.uk/ncdr/database/")

es = Elasticsearch([f'https://{elastic_username}:{elastic_password}@elastic.datalens.naimuri.dev:9200'])

if database_list_get.status_code == 200:

    database_list = BeautifulSoup(database_list_get.text, "html.parser").find_all("div", {"class": "col-md-4 card"})

    elastic_batch = []

    for database in database_list:
        try:
            logging.info("starting: " + database.find("p").get_text(strip=True))
            database_link = database.find('a')['href']
            database_title = database.find("p").get_text(strip=True)

            base_url = "https://data.england.nhs.uk"

            record = {
                'db_title': database_title,
                'db_url_path': base_url + database_link,
                'source': "NHS England NCDR Reference Library",
                'source_url': "https://data.england.nhs.uk/ncdr/database/",
                'ingest.timestamp': datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
            }

            # GET the next page containing tables + add description + get table list
            database_table_list_get = get_page(base_url + database_link)

            if database_table_list_get.status_code == 200:
                parsedDatabaseDataUrl = BeautifulSoup(database_table_list_get.text, "html.parser")

                record['db_description'] = parsedDatabaseDataUrl.select_one(
                    ".nhs-england-well > .col-md-12").text.strip()

                table_list = parsedDatabaseDataUrl.find_all("a", {"class": "table-link"})
                for table in table_list:
                    table_name = table.contents[0].strip()

                    record['table_name'] = table_name
                    record['table_url'] = base_url + table['href']
                    record['title'] = database_title + " / " + table_name

                    # GET the next page containing columns
                    parsed_table_url = get_page(base_url + table['href'])

                    if parsed_table_url.status_code == 200:

                        parsedTableUrl = BeautifulSoup(parsed_table_url.text, "html.parser")

                        record['table_description'] = parsedTableUrl.find("div",
                                                                          {"class": "row nhs-england-well"}).get_text(
                            strip=True)

                        column_list = parsedTableUrl.find_all("span", {"class": ""})
                        columns = []

                        for column in column_list:
                            columnToAdd = {'name': column.contents[1].contents[0].strip(),
                                           'url': base_url + column.contents[1]['href']}
                            columns.append(columnToAdd)
                        record['columns'] = columns
                        logging.info("Finished: " + table_name + " Pushing to elastic")

                        # Find and store entities.
                        entities_ = get_entities(record, ["db_title", "db_description", "table_name", "title"])
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
                bulk(es, elastic_batch, index=elastic_index)
            else:
                continue
        except AttributeError as ex:
            logging.error(ex)
            continue
else:
    logging.error("initial request failed for: " + database_list_get.url)
