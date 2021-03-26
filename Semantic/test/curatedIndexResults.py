import requests
import pprint
import numpy
import pandas as pd
from urllib.parse import quote

DESIRED_FILE_PATH = '/desired.csv'
RESULTS_WRITE_FILE_PATH = '/Users/alex.vandenbos/code/RESULTS.csv'

cols = [1]
desired = pd.read_csv(DESIRED_FILE_PATH)
RESULTS = desired[desired.columns[cols]]

for n in range(2, len(desired.columns)):
    QUERY = desired.columns[n]
    QUERY_SQL = quote(QUERY)

    # Send request and query to API.
    r = requests.get('http://127.0.0.1:5000/semantic/search?query=' + QUERY_SQL)
    results = r.json()

    # Create list to store scores
    scores = []

    # Remove unneeded keys from results.
    for i in range(len(results)):
        del results[i]['_source']
        del results[i]['_index']
        del results[i]['_type']
        scores.append(results[i]['_score'])

    # Calculate mean and standard deviation
    mean = numpy.mean(scores)
    sd = numpy.std(scores)

    # Calculate z scores for every result and store in analysedResults.
    analysedResults = results
    for i in range(len(analysedResults)):
        analysedResults[i]['zScore'] = ((analysedResults[i]['_score']) - mean)/sd
        del analysedResults[i]['_score']

    pprint.pprint(analysedResults)

    # Read csv as dataframe which stores the desired / undesired results.
    desired = pd.read_csv(DESIRED_FILE_PATH)
    positions = (desired.columns == QUERY)

    # Find the column which holds the given query.
    for i in range(len(positions)):
        if positions[i]:
            queryPosition = i
            print(queryPosition)
            break

    # Make new data frame with id, z score, desired(binary) for the given query.
    cols = [0, 1, queryPosition]
    finalResults = desired[desired.columns[cols]]

    # Match z scores with correct docs
    for i in range(len(analysedResults)):
        ar = analysedResults[i]['_id']
        zScore = analysedResults[i]['zScore']
        finalResults.loc[finalResults[finalResults.columns[0]] == ar, QUERY + ' zScore'] = zScore

    # Output final dataframe.
    cols = [2, 3]
    RESULTS = pd.concat([RESULTS, finalResults[finalResults.columns[cols]]], axis=1)

print(RESULTS)
RESULTS.to_csv(RESULTS_WRITE_FILE_PATH)



