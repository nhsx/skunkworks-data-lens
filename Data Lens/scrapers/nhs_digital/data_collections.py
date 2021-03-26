import json
import logging
import random
import sys
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from requests.adapters import HTTPAdapter, Retry
import entities

# Get elastic creds, index and filters from command arguments.
elastic_username = sys.argv[1:][0]
elastic_password = sys.argv[2:][0]
elastic_index = sys.argv[3:][0]


today = datetime.now().date()
logging.FileHandler('logs/%s.log' % today, mode='a', encoding=None, delay=False)
logging.basicConfig(filename='logs/%s.log' % today, level=logging.INFO, format="%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")


def get_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response
    except requests.HTTPError as exception:
        logging.error(exception)


def build_up_elastic_structure(html):
    if html is not None:
        object_to_be_built_up = {'html': str(html)}

        tables = html.select('div > table')
        p_tags = html.select('div > p')
        ordered_list_tags = html.select('article > p')
        unordered_list_tags = html.select('article > p')

        p_tags += ordered_list_tags + unordered_list_tags

        if tables:
            for table in tables:
                object_to_be_built_up['table' + "_" + str(random.randint(0, 9))] = table_section(table)

        combined_string = ""

        for p in p_tags:
            combined_string += p.get_text().strip() + " "
            object_to_be_built_up['strings'] = combined_string

        return object_to_be_built_up


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

    try:
        r = http.post(semantic_url, data=json.dumps(data), headers=headers)
        return eval(r.text) if isinstance(eval(r.text), str) else None
    except requests.HTTPError as exception:
        logging.error(exception)


def get_entities(data):
    if "title" in data and "introduction" in data:
        entities__ = entities.entities(' '.join([data['title'], data['introduction']]))
    else:
        entities__ = entities.entities(data['title'])
    ent_dict = {k: v for k, v in entities__.items() if v}
    return ent_dict


def table_section(table_html):
    if table_html is not None:
        table_data = []

        if len(table_html.find_all("td")) > 1:
            date_headers = table_html.find_all("th")
            data_rows = table_html.find_all("tr")

            for date_row in data_rows:
                data = date_row.find_all("td")
                date_object = dict()

                if len(data) > 0:
                    for i in range(0, len(date_headers)):
                        date_object[date_headers[i].get_text().strip()] = data[i].get_text().strip()
                    table_data.append(date_object)

        return table_data


base_page = "https://digital.nhs.uk/data-and-information/data-collections-and-data-sets/data-collections"

base_page_get = get_page(base_page)

if base_page_get.status_code == 200:

    logging.info("starting scraping " + datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3])

    es = Elasticsearch([f'https://{elastic_username}:{elastic_password}@elastic.datalens.naimuri.dev:9200'])
    elastic_batch = []
    results = BeautifulSoup(base_page_get.text, "html.parser").find_all("div", {"class": "cta"})

    for result in results:
        # Follow the collection URL and parse the page
        parsed_search_get = get_page("https://digital.nhs.uk" + result.find("a")['href'])

        if parsed_search_get.status_code == 200:
            parsed_search_result = BeautifulSoup(parsed_search_get.text, "html.parser")

            dates = parsed_search_result.find_all("div",
                                                  {"data-uipath": "website.contentblock.section.content"})
            title = parsed_search_result.find("h1", {"data-uipath": "document.title"})
            introduction = parsed_search_result.find("div", {"data-uipath": "website.general.summary"})

            # Set initial values
            record = {
                "url": "https://digital.nhs.uk" + result.find("a")['href'],
                "source": "NHS Digital",
                "source_url": base_page,
                "ingest.timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3],
                "type": "Data Collection"
            }

            if title:
                record['title'] = title.get_text().strip()

            if introduction and introduction.get_text().strip():
                record['introduction'] = introduction.get_text()

            # Call semantic end point and get vectors.
            vectors = get_vectors(record)
            if vectors:
                record['text_vector'] = json.loads(vectors)

            # Find and store entities.
            entities_ = get_entities(record)
            if entities_:
                record["entities"] = entities_

            # for common_id in list_of_common_ids:
            id_data = parsed_search_result.find_all("div", {"class": "article-section navigationMarker"})

            if id_data:
                for section in id_data:
                    key = section.find("h2").get_text().strip() if section.find("h2") else random.randint(0, 9)
                    record[section.find("h2").get_text().strip()] = build_up_elastic_structure(section.find("div", {"class": "rich-text-content"}))

            elastic_batch.append(record)

            if len(elastic_batch) == 100:
                # Send the search result to elastic search and clear the list
                bulk(es, elastic_batch, index=elastic_index)
                elastic_batch.clear()
        else:
            continue

    # Send the search result to elastic search and clear the list
    bulk(es, elastic_batch, index=elastic_index)
    elastic_batch.clear()

else:
    logging.error("Base page request failed code: " + str(base_page_get.status_code))
