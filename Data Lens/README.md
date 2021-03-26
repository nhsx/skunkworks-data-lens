# Data Lens

Project Structure

PLEASE do a `pip3 / pip install -r Requirements.txt` before running any code.

/com205_entity_extractor
- This contains all code for extracting entities. To be used it run the following command 
  
- If after installing the pip packages from Requirements.txt you are still having issues then run `pip3 install -e com205_entity_extractor/`

/com205_entity_extractor_lambda
- This contains the code for the entity code but in AWS lambda form.

nifi/groovy
- This contains all groovy scripts for the Nifi flows, they have been grouped by each flow

/scrapers
- This contains all scraper code, each folder is a source and within them is the scaper(s) and a log file. Each
scraper will log to that file.
  
nifi/flow
- This contains an export of the nifi flow. This can be uploaded to nifi.