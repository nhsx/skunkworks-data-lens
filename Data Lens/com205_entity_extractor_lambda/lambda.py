import json
import io
import os
import re

def lambda_handler(event, context):


    data = event['body']
    sep ='\t'
    comment ='#'
    encoding ='utf-8'
    skip = 0

    print(data)

    cities = []
    counties = []
    countries = []

    with io.open("./uk_counties_list.txt",'r', encoding=encoding) as f:

        # filter comment lines
        lines = (line for line in f if not line.startswith(comment))


        for line in lines:
            columns = line.split(sep)
            city = columns[0].rstrip('\n')
            county = columns[1].rstrip('\n')
            country = columns[2].rstrip('\n')

            if re.search(fr'\b{city}\b', data):
                cities.append(city)
                counties.append(county) if county not in counties else None
                countries.append(country) if country not in countries else None
            elif re.search(fr'\b{county}\b', data) and county not in counties:
                counties.append(county)
                countries.append(country) if country not in countries else None
            elif re.search(fr'\b{country}\b', data) and country not in countries:
                countries.append(country)

    with io.open("nhs_trust_list.txt", 'r', encoding=encoding) as trust_list_file:

        # filter comment lines
        trust_list = (line.strip("\n") for line in trust_list_file if not line.startswith(comment))
        trusts = [trust for trust in trust_list if trust.lower() in data.lower()]

    with io.open("uk_university_list.txt", 'r', encoding=encoding) as university_list_file:

        # filter comment lines
        university_list = (line.strip("\n") for line in university_list_file if not line.startswith(comment))
        universities = [uni for uni in university_list if uni.lower() in data.lower()]

    return {
        "statusCode": 200,
        "body": json.dumps({"cities": cities, "counties": counties, "countries": countries, "trusts": trusts, "universities": universities})
    }


