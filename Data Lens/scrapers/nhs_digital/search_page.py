import json
import logging
import re
import sys
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from requests.adapters import HTTPAdapter, Retry
import entities

# Get elastic credentials, index and filters from command arguments.
elastic_username = sys.argv[1:][0]
elastic_password = sys.argv[2:][0]
document_type_filters = sys.argv[4:]
elastic_index = sys.argv[3:][0]

es = Elasticsearch([f'https://{elastic_username}:{elastic_password}@elastic.datalens.naimuri.dev:9200'])
base_url = "https://digital.nhs.uk"
elastic_batch = []


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


def list_of_strings(html):
    list_of_text = html.findAll(text=True)
    formatted_list_strings = []
    for list_item in list_of_text:
        if list_item != " " and list_item != "\n":
            split_list = list_item.split("\n")
            for item in split_list:
                formatted_list_strings.append(item)
    return formatted_list_strings


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



def get_resources(data):
    resource_list = []
    for resource in data:
        link = resource.find("a")
        data = {"title": link["title"], "url": link["href"]}
        resource_list.append(data)
    return resource_list


def get_datasets(data):
    dataset_list = []
    for data_set in data:
        link = data_set.find("a", {"itemprop": "url"})
        data = {"title": link["title"], "url": base_url + link["href"]}
        dataset_list.append(data)
    return dataset_list


def loop_through_results(results):
    for search_result in results:
        link_to_search_result_data = base_url + search_result.find("a", {"class": "cta__title cta__button"})['href']
        title_of_search_result = search_result.find("a", {"class": "cta__title cta__button"})['title']

        search_result_request = get_page(link_to_search_result_data)

        if search_result_request.status_code == 200:
            # Follow the search result and continue building up the elastic search object

            parsed_search_result_url = BeautifulSoup(search_result_request.text, "html.parser")

            # I wanted to stick to gathering all data from the search result page, however, some pages may be broken in which case I have took the value from the search result.
            title = parsed_search_result_url.find("meta", property='og:title')[
                "content"] if parsed_search_result_url.find("meta", property='og:title') else title_of_search_result
            result_url = parsed_search_result_url.find("meta", property='og:url')[
                "content"] if parsed_search_result_url.find("meta", property='og:url') else link_to_search_result_data

            # Add items to send to elastic
            # Clear the dict
            record = {"title": title,
                      "url": result_url,
                      "source": "NHS Digital",
                      "source_url": "https://digital.nhs.uk/search",
                      "ingest.timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3],
                      "type": document_filter
                      }

            #####
            # Introduction #
            ####
            # Get data from page (tried to use meta data where I can)
            introduction = parsed_search_result_url.find("meta", {"name": "description"}),
            if introduction[0]:
                record["introduction"] = introduction[0]['content']

            #####
            # Description #
            ####
            # parse Description
            description = parsed_search_result_url.find("div", {"itemprop": "description"})
            if description:
                record["description"] = list_of_strings(description)


            #####
            # Entities #
            ####
            # Find and store entities.
            entities_ = get_entities(record, ["title", "introduction"])
            if entities_:
                record["entities"] = entities_

            #####
            # Key Findings #
            ####
            # for key findings the format can be vastly different, to account for this we have experimentally stored
            # the html for rendering in the front end as well as strings to be used for search.
            # we removed images as those are not saved.
            key_findings = parsed_search_result_url.find("div", {"class": "callout--attention"})
            if key_findings:
                key_findings_dict = {"html": re.sub(r'(<img([\w\W]+?)>)', "", str(key_findings).replace("\n", "")),
                                     "strings": list_of_strings(key_findings)}
                record["key_findings"] = key_findings_dict

            #####
            # DATES #
            ####
            date_published = parsed_search_result_url.find("dd", {"itemprop": "datePublished"})
            if date_published:
                record["date_published"] = date_published.get_text().strip()

            # parse spatial coverage
            spatial_coverage = parsed_search_result_url.find("dd", {"itemprop": "spatialCoverage"})
            if spatial_coverage:
                record["spatial_coverage"] = spatial_coverage.get_text().strip()

            # Normalise dates to be the same format as NHS Data Catalogue
            temporal_coverage = parsed_search_result_url.find("meta", {"itemprop": "temporalCoverage"})
            if temporal_coverage:
                date_split = temporal_coverage['content'].split('/')
                coverage_start_date = date_split[0]
                coverage_end_date = date_split[1]
                _dict = {}

                if coverage_start_date:
                    _dict["coverage_start_date"] = coverage_start_date

                if coverage_end_date:
                    _dict["coverage_end_date"] = coverage_end_date

            #####
            # Data Sets #
            ####
            # Some publications have the data sets linked, so I will add them
            data_sets = parsed_search_result_url.find_all("li", {"itemtype": "http://schema.org/Dataset"})
            # check if data sets where found then add them to a list
            if data_sets:
                record["datasets"] = get_datasets(data_sets)

            #####
            # Resources #
            ####
            # check if resources where found then add them to a list
            resources = parsed_search_result_url.find_all("li", {"itemtype": "http://schema.org/DataDownload"})
            if resources:
                record["resources"] = get_resources(resources)

            #####
            # Publications #
            ####
            # get publications for datasets
            if document_filter == "dataset":
                publication_link = parsed_search_result_url.find("span", {"class": "article-header__label"})

                record['publication_name'] = publication_link.find("a")['title']
                record['publication_url'] = base_url + publication_link.find("a")['href']

            #####
            # Vectors #
            ####
            # Call semantic end point and get vectors.
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


def start_scraping(url):
    page = 1
    keep_scraping = True

    while keep_scraping:
        try:
            true_url = url.replace("REPLACE", str(page))

            logging.info("Page number: " + str(page))

            # Parse page after selecting type and date filter
            search_result_request = get_page(true_url)
            if search_result_request.status_code == 200:
                search_result_page = BeautifulSoup(search_result_request.text, "html.parser")
                # Results can be either cta detailed or cta stamped ... look for both and put them into one list.
                list_of_search_results = search_result_page.find_all("div", {"class": "cta cta--detailed"})
                list_of_stamped_results = search_result_page.find_all("div",
                                                                      {"class": "cta cta--detailed cta--stamped"})
                search_results = list_of_search_results + list_of_stamped_results

                # Website allows you to keep going through pages as it just returns the last set of results over and
                # over again, however, the next button seems to disappear when it gets to the last page of results.
                # so I am going to use this to determine if we should keep scraping.
                next_button = search_result_page.find("a", {"title": "Next"})

                # start looping through the results
                loop_through_results(search_results)

                # Check if next button is on the page, if not then assume no more results and break.
                if next_button is None:
                    logging.info(
                        "No more entries, I am going to stop scraping. " + "The page number I got to was " + str(page))
                    keep_scraping = False

                    # Send remaining docs
                    bulk(es, elastic_batch, index=elastic_index)
                    elastic_batch.clear()
                else:
                    page += 1
            else:
                page += 1
                continue
        except Exception as ex:
            logging.error(ex)


for document_filter in document_type_filters:
    logging.info("starting scraping " + datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3])
    logging.info('Selected filter: ' + document_filter)
    document_filter_url = "https://digital.nhs.uk/search/document-type/%s" % document_filter

    filtered_search_get = get_page(document_filter_url)

    if filtered_search_get.status_code == 200:
        filtered_search_page = BeautifulSoup(filtered_search_get.text, "html.parser")
        list_of_date_filters = filtered_search_page.find("ul", {"title": "PUBLICATION YEAR"})

        # Some type filters have additional date filters whilst others don't.
        if list_of_date_filters is not None:
            list_of_date_filters = list_of_date_filters.find_all("a", {"class": "filter-link"})
            for date_filter in list_of_date_filters:
                logging.info('Selected date filter: ' + date_filter.getText())
                start_scraping(
                    "https://digital.nhs.uk/search/document-type/%s/year/%s?r61_r2:page=REPLACE&r61_r2:pageSize=10" % (
                        document_filter, date_filter["title"]))
        else:
            start_scraping("https://digital.nhs.uk/search/document-type/%s?r61_r2:page=REPLACE&r61_r2:pageSize=10" % (
                document_filter))
    else:
        continue
