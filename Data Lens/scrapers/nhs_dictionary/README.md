
This script scrapes the NHS Dictionary data and inserts it into Elastic search.

Script starts at https://datadictionary.nhs.uk/

The script works by getting going to various pages on the site that have a similar structure
it goes to each section and then gets a list of sections from that page and then processes them 1 by 1 and then 
adds them to a list, the list is then batched to elastic Search and the script continues.

An example of JSON data sent to elastic search ...

`{
        "_index" : "c205-nhs-data-dictionary",
        "_type" : "_doc",
        "_id" : "91CoXncBBq4JYfWNlFNc",
        "_score" : 9.9290075E-5,
        "_source" : {
          "title" : "Court",
          "description" : "A Court is a building in which legal proceedings are heard and people can be securely detained during the trial process.",
          "type" : "NHS Business Definition",
          "url" : "https://datadictionary.nhs.uk/nhs_business_definitions/court.html",
          "source" : "NHS Data Dictionary",
          "source_url" : "https://datadictionary.nhs.uk/nhs_business_definitions_overview.html",
          "ingest.timestamp" : "2021-02-01T17:34:02.216",
          "plural" : "Courts"
        }
      }`


