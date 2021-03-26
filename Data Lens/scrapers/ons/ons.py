import json
import logging
import sys
import datetime
import time
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
import requests

# Command line arguments
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

    try:
        source = data['source'].replace(" ", "%20")
    except Exception as ex:
        logging.error(ex)

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


def get_page(url: str) -> BeautifulSoup:
    return BeautifulSoup(requests.get(url, headers={
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Bot'
    }).text, 'html.parser')


def parse_category(url: str):
    parsed_page = get_page(url)

    tiles = parsed_page.find('div', {"class": "tiles"}).find_all('li')
    tiles.pop()  # Remove the local statistics tile as this doesn't contain searchable datasets.

    for category in tiles:
        parse_data_publications(baseURL + category.find('a', href=True)['href'])


def parse_data_publications(url: str):
    parsed_page = get_page(url)

    data_links = parsed_page.find('nav', {"aria-label": "Related content"}).find_all('li')

    for link in data_links[:2]:
        parse_results(baseURL + link.find('a', href=True)['href'], link.find('a', href=True)['href'])


def parse_results(url: str, appended_url: str):
    parsed_page = get_page(url + "?:uri=" + appended_url[1:] + "&size=10000")

    results = parsed_page.find('div', {"class": "results"}).find_all('li')
    elastic_batch = []
    for result in results:

        record = dict()

        # Get data from the search results because it's the only place with a tiny bit of consistency
        title = result.find('span', {'role': 'text'})
        keywords = result.find('p', {'class': 'search-results__keywords'})
        results_meta = result.find('p', {'class': 'search-results__meta'})
        results_description = result.find('div', {'class': 'search-results__summary'})

        record['source'] = "Office for National Statistics"
        record['source_url'] = "https://www.ons.gov.uk/search"
        record["ingest.timestamp"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]

        if title:
            record['title'] = title.text.strip()

        if results_description:
            if results_description.text != '\n':
                record['description'] = results_description.text.strip()

        if results_meta:
            data_type = results_meta.text.split('|')[0].strip()
            record['type'] = data_type

        if keywords:
            keywords_list = [kw.strip() for kw in
                             keywords.text[10:].split(',')]  # Split into list and remove leading spaces and trailing /n
            record['keywords'] = keywords_list

        vectors = get_vectors(record)
        if vectors:
            record['text_vector'] = json.loads(vectors)

        result_url = result.find('a', href=True)
        if result_url:
            parse_result(result_url['href'], record)

        entities_ = get_entities(record, ["title", "introduction"])
        if entities_:
            record["entities"] = entities_

        resultsList.append(record)
        elastic_batch.append(record)

        if len(elastic_batch) == 100:
            bulk(es, elastic_batch, index=elastic_index)
            elastic_batch.clear()

        time.sleep(0.5)
    bulk(es, elastic_batch, index=elastic_index)
    elastic_batch.clear()

    with open('data.json', 'w') as f:
        json.dump(resultsList, f)

    return None


def parse_result(url, record):
    parsed_result = get_page(baseURL + url)

    record['url'] = baseURL + url

    dataset_downloads = parsed_result.find_all('div', {'class': 'show-hide'})
    pdf_downloads = parsed_result.find_all('a', {'class': 'js-pdf-dl-link'})
    user_request_downloads = parsed_result.find_all('ul', {'class': 'list--neutral'})
    main_points = parsed_result.find('div', {'id': 'main-points'})
    main_findings = parsed_result.find('div', {'id': 'main-findings'})
    meta_wrap_data = parsed_result.find_all('p', {'class': 'meta__item'})
    secondary_meta = parsed_result.find_all('p', {'class': 'page-neutral-intro__meta'})
    page_bulletins = parsed_result.find('div', {'class': 'page-bulletins'})
    article_data = parsed_result.find('article')
    toc = parsed_result.find('div', {'class': 'table-of-contents'})

    if meta_wrap_data:
        for meta_item in meta_wrap_data:
            meta_split = meta_item.text.split(':')
            try:
                content = datetime.datetime.strptime(meta_split[1].strip(), '%d %B %Y').date().isoformat()
            except ValueError:
                if meta_split[0].lower().replace(' ', '_').strip() == "next_release":
                    continue
                content = meta_split[1].strip()
            record[meta_split[0].lower().replace(' ', '_').strip()] = content

    if page_bulletins:
        meta_wrapper = page_bulletins.find_all('div', {'class': 'wrapper'})[2]
        meta_items = meta_wrapper.find_all('p')
        for meta_item in meta_items:
            meta_split = meta_item.text.split(':')
            try:
                content = datetime.datetime.strptime(meta_split[1].strip(), '%d %B %Y').date().isoformat()
            except ValueError:
                if meta_split[0].lower().replace(' ', '_').strip() == "next_release":
                    continue
                content = meta_split[1].strip()
            record[meta_split[0].lower().replace(' ', '_').strip()] = content

    if secondary_meta:
        for meta in secondary_meta:
            try:
                content = datetime.datetime.strptime(meta.text.strip(), '%d %B %Y').date().isoformat()
                record['release_date'] = content
            except ValueError:
                if meta_split[0].lower().replace(' ', '_').strip() == "next_release":
                    continue
                content = meta.text.strip()
                record['meta_data'] = content

    if main_points:
        main_points_str = ""
        for p in main_points.find_all('p'):
            main_points_str += p.text + "\n "
        record['main_points'] = main_points_str

    if not main_points and main_findings:
        main_points_str = ""
        for p in main_findings.find_all('p'):
            main_points_str += p.text + "\n "
        record['main_points'] = main_points_str

    if dataset_downloads:
        download_objects = []
        for download in dataset_downloads:
            download_object = {}

            if download.has_attr('id'):
                download_object['title'] = download['id']
                download_url = download.find('a')
                if download_url:
                    download_object['url'] = baseURL + download_url['href']
                    download_objects.append(download_object)

        record['resources'] = download_objects

    if user_request_downloads and not 'resources' in record:
        for user_request_download in user_request_downloads:
            download_objects = []
            download_links = user_request_download.find_all('a', {"data-gtm-type": "related-download"}, href=True)
            for link in download_links:
                download_objects.append({'title': link.text.strip(), 'url': baseURL + link['href']})
            record['resources'] = download_objects

    if pdf_downloads:
        pdf_objects = []
        for pdf_link in pdf_downloads:
            pdf_objects.append({'title': 'PDF Download', 'url': baseURL + pdf_link['href']})

        if 'resources' in record:
            record['resources'] += pdf_objects
        else:
            record['resources'] = pdf_objects

    if article_data and 'description' not in record:
        summary = article_data.find('div', {'class': 'section__content--static-markdown'})
        if summary:
            record['description'] = summary.find('p').text

    if toc and not article_data:
        chapters = []
        chapter_url = parsed_result.find_all('a', {'class': 'chapter'})
        for chapter in chapter_url:
            chapter_dict = dict()

            parse_result(chapter['href'], chapter_dict)

            chapters.append(chapter_dict)

        record['chapters'] = chapters


resultsList = []
baseURL = "https://www.ons.gov.uk"
health_and_social_care_url = "https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare"

logging.info("starting scraping " + datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3])

parse_category(health_and_social_care_url)

logging.info("Finished Scraping")
