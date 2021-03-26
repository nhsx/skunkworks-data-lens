const {
        simpleQuery, 
        simpleQueryTypes,
        simpleQueryFilterOptions,
        simpleQueryDataDictionary,
        addClickLog,
        addSearchLog,
        idLookup,
        } = require('../utils/ElasticRequests');
const { TranslateClient, TranslateTextCommand } = require("@aws-sdk/client-translate");
const { simpleQueryResultBuilder, semanticQueryResultBuilder } = require('../utils/QueryResultBuilder');
const {
    getSearchAndFilterResults,
    getRecommendations
    } = require('../utils/SemanticRequests');

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

        if (multiLangEnabled){
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
        
        if(resultNumber == 0){
            queryResults = await simpleQuery(req.elasticClient, query, page || 1, contentType, filters, exactMatch_false);
            resultNumber = queryResults["body"]["hits"]["hits"].length;
        }

        if(resultNumber == 0){
            var semanticQueryResults = await getSearchAndFilterResults(query);
            res.send(semanticQueryResultBuilder(semanticQueryResults));
        }

        const queryTypes = await simpleQueryTypes(req.elasticClient, query, filters);
        const queryFilters = await simpleQueryFilterOptions(req.elasticClient, query, filters);
        const queryDataDictionary = await simpleQueryDataDictionary(req.elasticClient, query, filters);
        const searchLog = await addSearchLog(req.elasticClient, userid, query, page, queryResults["body"]["hits"]["hits"]);
        res.send(simpleQueryResultBuilder(queryResults, queryTypes, queryFilters, queryDataDictionary, sourceLanguageCode));
    } catch(error){
        next(error);
    }
}

exports.addClickLog = async(req, res, next) => {
    try{
        var result = await addClickLog(req.elasticClient, req.body);
        res.status(result.statusCode).send();
    } catch(error){
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

function sendQuery(deviceQuery, res, isAggregation) {
    if(deviceQuery["body"]["hits"].length === 0){
        res.status(404).send();
    } else if(isAggregation) {
        res.send(deviceQuery["body"]["aggregations"]["summary"]["content"]["buckets"]);
    } else {
        res.send(deviceQuery["body"]["hits"]["hits"]);
    }
}
