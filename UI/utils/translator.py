from pygoogletranslation import Translator
import json
import sys
import time
import datetime
import time
from elasticsearch import Elasticsearch

# Command line argumments
# elastic_username = sys.argv[1:][0]
# elastic_password = sys.argv[2:][0]
# elastic_index = sys.argv[3:][0]
file = open("languages.txt", 'w')

translator = Translator()

# All language codes that both amazon and google support
countryCodes = ["af","sq","am","ar","hy","az","bn","bs","bg","ca",
                "hr","cs","da","nl","en","et","fa","tl",
                "fi","fr","ka","de","el","gu","ht","ha","he","hi",
                "hu","is","id","it","ja","kn","kk","ko","lv","lt","mk","ms",
                "ml","mt","mn","no","fa","ps","pl","pt","ro","ru","sr","si",
                "sk","sl","so","es","sw","sv","tl","ta","te","th","tr",
                "uk","ur","uz","vi","cy"]

result_dict = dict()
for code in countryCodes:

    result_dict[code] = {}

    result_dict[code]['title'] = translator.translate('Language Support', dest=code, src="en").text
    result_dict[code]['selectLabel'] = translator.translate('Choose Instruction Language', dest=code, src="en").text
    result_dict[code]['headerLine'] = translator.translate('Please change your language by following the settings below', dest=code, src="en").text

    result_dict[code]['list'] = {}

    result_dict[code]['list']['chrome'] = [] 
    results = translator.translate([
                  "At the top right, click More. Then Settings.",
                  "At the bottom, click Advanced.",
                  "Under 'Languages,' click Language.",
                  "Next to the language you'd like to use, click More.",
                  "Turn Offer to translate pages in this language on or off."], dest=code, src="en")

    print(code)
    for result in results:
        result_dict[code]['list']['chrome'].append(result.text)

    result_dict[code]['list']['safari'] = [] 
    results = translator.translate([
                  "Your Language must be chosen within the computer settings.",
                  "Within the searchbar there will be a Translate Icon.",
                  "Select your chosen Language from the dropdown menu."], dest=code, src="en")
    print(result)
    for result in results:
        result_dict[code]['list']['safari'].append(result.text)

    result_dict[code]['list']['other'] = translator.translate("Please use a browser with translation services, we have a helpful step by step guide for use within Chrome and Safari.", dest=code, src="en").text
    
    result_dict[code]['checkBox'] = translator.translate("Don't show this again", dest=code, src="en").text
    result_dict[code]['confirmButton'] = translator.translate("Confirm", dest=code, src="en").text

file.write(json.dumps(result_dict))