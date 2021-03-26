exports.simpleQueryResultBuilder = (result, types, filters, dataDictionary, sourceLanguageCode) => {
    const returnObject = {};
    console.log(result);
    console.log("FILTERS")
    console.log(JSON.stringify(filters["body"]["aggregations"]));
    console.log(JSON.stringify(filters["body"]["aggregations"]["source_agg"]["buckets"]));
    returnObject["total"] = result["body"]["hits"]["total"].value;
    returnObject["hits"] = result["body"]["hits"]["hits"];
    returnObject["pages"] = Math.ceil(result["body"]["hits"]["total"]["value"] / 20);
    if(dataDictionary["body"]["hits"]["total"].value > 0){
        returnObject["dictionary"] = dataDictionary["body"]["hits"]["hits"].map(el => {
            el._source.description = el._source.description.replace(/Â/g, "")
            return el
            });
    }
    returnObject["filters"] = {};
    returnObject["filters"]["source"] = filters["body"]["aggregations"]["source_agg"]["buckets"].map(bucket => bucket.key);
    returnObject["filters"]["author"] = [...new Set(types["body"]["hits"]["hits"].map(hit => "author" in hit["_source"] ? hit["_source"]["author"] : "No Author"))];
    returnObject["filters"]["license_title"] = [...new Set(types["body"]["hits"]["hits"].map(hit => "license_title" in hit["_source"] ? hit["_source"]["license_title"] : "No Licence Title"))];
    returnObject["filters"]["type"] = [...new Set(types["body"]["hits"]["hits"].map(hit => "type" in hit["_source"] ? hit["_source"]["type"] : "No Type"))];
    returnObject["filters"]["title"] = [...new Set(types["body"]["hits"]["hits"].map(hit => "title" in hit["_source"] ? hit["_source"]["title"] : "No Title"))];
    if(sourceLanguageCode != ""){
        returnObject["sourceLanguageCode"] = sourceLanguageCode;
    }

    return returnObject;
}

exports.semanticQueryResultBuilder = (result) => {
    const returnObject = {};

    returnObject["total"] = result.length;
    returnObject["hits"] = result;

    returnObject["filters"] = {};
    returnObject["filters"]["source"] = [...new Set(result.map(hit => "source" in hit["_source"] ? hit["_source"]["source"] : "No Source"))];
    returnObject["filters"]["license_title"] = [...new Set(result.map(hit => "source" in hit["_source"] ? hit["_source"]["source"] : "No Licence Title"))];
    returnObject["filters"]["type"] = [...new Set(result.map(hit => "source" in hit["_source"] ? hit["_source"]["source"] : "No Type"))];

    return returnObject;

}