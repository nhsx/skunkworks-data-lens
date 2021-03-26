const { getOperationInfo,
        simpleQuery, 
        simpleQueryTypes,
        simpleQueryFilterOptions,
        simpleQueryDataDictionary,
        addClickLog,
        addSearchLog,
        idLookup,
        closestCalendarEvents,
        customQuery,
        bulkQuery} = require('../utils/ElasticRequests');
//const { calculateTopContacts } = require('../utils/TopCallsCalculator');
const { TranslateClient, TranslateTextCommand, TextSizeLimitExceededException } = require("@aws-sdk/client-translate");
const { simpleQueryResultBuilder, semanticQueryResultBuilder } = require('../utils/QueryResultBuilder');
const {
    getSearchAndFilterResults,
    getRecommendations
    } = require('../utils/SemanticRequests');

exports.getInfo = async (req, res, next) =>  {
    try{
        res.send(await req.elasticClient.info());
    } catch(error){
        next(error);
    }
}

exports.simpleQuery = async(req, res, next) => {
    const exactMatch_true = true;
    const client = new TranslateClient({"region": "eu-west-2"});
    const exactMatch_false = false;
    try{
        let {
            query,
            page,
            contentType,
            filters,
            userid,
            multiLangEnabled
        } = req.body;
        let sourceLanguageCode = "";

        if(page && page <=0) {
            res.status(401).send("Page value cannot be below 1");
        }

        console.log("REQUEST BODY")
        console.log(req.body)

        if (multiLangEnabled){
            console.log("MULTI ENABLED")
            const params = {
                Text: query,
                SourceLanguageCode: "auto",
                TargetLanguageCode: "en"
            };
            const command = new TranslateTextCommand(params);

            const translateResult = await client.send(command);
            query = translateResult.TranslatedText;
            sourceLanguageCode = translateResult.SourceLanguageCode;
        }

        var queryResults = await simpleQuery(req.elasticClient, query, page || 1, contentType, filters, exactMatch_true);
        var resultNumber = queryResults["body"]["hits"]["hits"].length;
        let temp = queryResults["body"]["hits"]["total"].value;

        console.log("HITS = " + resultNumber)
        console.log("TOTAL = " + temp)
        
        if(resultNumber == 0){
            console.log("Fuzzy Search");
            queryResults = await simpleQuery(req.elasticClient, query, page || 1, contentType, filters, exactMatch_false);
            resultNumber = queryResults["body"]["hits"]["hits"].length;
            console.log(queryResults);
            console.log(queryResults["body"]["hits"]);
            console.log(resultNumber);
        }

        if(resultNumber == 0){
            console.log("Semantic Search");
            var semanticQueryResults = await getSearchAndFilterResults(query);
            res.send(semanticQueryResultBuilder(semanticQueryResults));
        }

        const queryTypes = await simpleQueryTypes(req.elasticClient, query, filters);
        const queryFilters = await simpleQueryFilterOptions(req.elasticClient, query, filters);
        const queryDataDictionary = await simpleQueryDataDictionary(req.elasticClient, query, filters);
        const searchLog = await addSearchLog(req.elasticClient, userid, query, page, queryResults["body"]["hits"]["hits"]);
        res.send(simpleQueryResultBuilder(queryResults, queryTypes, queryFilters, queryDataDictionary, sourceLanguageCode));
    } catch(error){
        console.log(error);
        next(error);
    }
}

exports.addClickLog = async(req, res, next) => {
    try{
        var result = await addClickLog(req.elasticClient, req.body);
        res.status(result.statusCode).send();
    } catch(error){
        console.log(error);
        console.log(JSON.stringify(error));
        next(error);
    }
}


exports.searchById = async(req, res, next) => {
    try{
        const result = await idLookup(req.elasticClient, req.params.id);
        sendQuery(result, res, false);
    } catch(error){
        console.log(error.body.error.reason)
        next(error);
    }
}

 exports.searchById = async(req, res, next) => {
     try{
         const result = await idLookup(req.elasticClient, req.params.id);
         const indexString = result["body"]["hits"]["hits"][0]["_index"];
         const idString = result["body"]["hits"]["hits"][0]["_id"];
         const recommendations = await getRecommendations(indexString, idString);
         result["body"]["hits"]["hits"][0]["_recommendations"] = recommendations;
         sendQuery(result, res, false);
     } catch(error){
         next(error);
     }
}

exports.closestCalendarEntries = async(req, res, next) => {
    try{
        const {
            imei,
            date
        } = req.body;
        const result = await closestCalendarEvents(req.elasticClient, date, imei);
        sendQuery(result, res, false)
    } catch(error){
        next(error);
    }
}

exports.customQuery = async(req, res, next) => {
    try {
        const result = await customQuery(req.elasticClient, req.params.index, req.body)
        sendQuery(result, res, false);
    } catch(error){
        next(error)
    }
}

exports.bulkQuery = async(req, res, next) => {
    try {
        return res.send(await bulkQuery(req.elasticClient, req.body))
    } catch(error){
        next(error)
    }
}

function sendQuery(deviceQuery, res, isAggregation) {
    if(deviceQuery["body"]["hits"].length === 0){
        res.status(404).send();
    } else if(isAggregation) {
        // console.log(deviceQuery);
        res.send(deviceQuery["body"]["aggregations"]["summary"]["content"]["buckets"]);
    } else {
        // console.log(deviceQuery);
        res.send(deviceQuery["body"]["hits"]["hits"]);
    }
}
