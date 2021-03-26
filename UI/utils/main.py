from pygoogletranslation import Translator
import json
import sys
import time
import datetime
import time
from elasticsearch import Elasticsearch

# Command line argumments
elastic_username = sys.argv[1:][0]
elastic_password = sys.argv[2:][0]
elastic_index = sys.argv[3:][0]

translator = Translator()

# All language codes that both amazon and google support
countryCodes = ["af","sq","am","ar","hy","az","bn","bs","bg","ca",
                "hr","cs","da","nl","en","et","fa","tl",
                "fi","fr","ka","de","el","gu","ht","ha","he","hi",
                "hu","is","id","it","ja","kn","kk","ko","lv","lt","mk","ms",
                "ml","mt","mn","no","fa","ps","pl","pt","ro","ru","sr","si",
                "sk","sl","so","es","sw","sv","tl","ta","te","th","tr",
                "uk","ur","uz","vi","cy"]

for code in countryCodes:

    result_dict = dict()

    result_dict['language'] = code

    result_dict['title'] = translator.translate('Language Support', dest=code, src="en").text
    result_dict['selectLabel'] = translator.translate('Choose Instruction Language', dest=code, src="en").text
    result_dict['headerLine'] = translator.translate('Please change your language by following the settings below', dest=code, src="en").text

    result_dict['list'] = {}

    result_dict['list']['chrome'] = [] 
    results = translator.translate([
                  "Your Language must be chosen within the chrome settings.",
                  "Within the searchbar there will be a Translate Icon.",
                  "Select your chosen Language from the dropdown menu."], dest=code, src="en")

    for result in results:
        result_dict['list']['chrome'].append(result.text)

    result_dict['list']['safari'] = [] 
    results = translator.translate([
                  "Your Language must be chosen within the computer settings.",
                  "Within the searchbar there will be a Translate Icon.",
                  "Select your chosen Language from the dropdown menu."], dest=code, src="en")

    for result in results:
        result_dict['list']['safari'].append(result.text)

    result_dict['checkbox'] = translator.translate("Don't show this again", dest=code, src="en").text
    result_dict['confirmButton'] = translator.translate("Confirm", dest=code, src="en").text

    # Uncomment to send to elastic, was commented out while I was testing
    #es = Elasticsearch([f'https://{elastic_username}:{elastic_password}@elastic.datalens.naimuri.dev:9200'])
    #es.index(index=elastic_index, doc_type='_doc', body=json.dumps(result_dict, ensure_ascii=False))