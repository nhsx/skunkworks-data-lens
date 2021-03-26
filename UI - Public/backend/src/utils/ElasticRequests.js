const indexString = 'com205-*';
const dataDictionaryIndexString = 'c205-nhs-data-dictionary';

exports.simpleQuery = async (elasticClient, queryString, page, contentTypeFilter, filters, exactMatch) =>  {
    const PAGE_SIZE = 20;
    const SPECIAL_CASE_NUMBERS = ['999', '111'];
    let queryBody = '';
    let queryStringArray = queryString.split(" ");
    queryString = '';
    for(arrayString of queryStringArray){
        queryString += arrayString;
        if(Number(arrayString)){
            if(!SPECIAL_CASE_NUMBERS.includes(arrayString)){
                queryString += "^0.5";
            }
        }
        queryString += " ";
    }
    if(exactMatch) {
        queryBody = {
            index: indexString,
            body: {
                "size": PAGE_SIZE, "from": PAGE_SIZE * (page - 1),
                "query": {
                    "bool": {
                        "should": [
                            {
                                "query_string": {
                                    "query": queryString,
                                    "type": "best_fields",
                                    "phrase_slop": 0,
                                    "default_operator": "AND",
                                    "fields": [
                                        "title^5",
                                        "*"
                                    ],
                                    "analyze_wildcard": true,
                                    "boost": 2
                                }
                            },
                            {
                                "query_string": {
                                    "query": queryString,
                                    "type": "best_fields",
                                    "default_operator": "AND",
                                    "fields": [
                                        "title^5",
                                        "*"
                                    ],
                                    "analyze_wildcard": true,
                                    "boost": 1.5
                                }
                            },
                            {
                                "query_string": {
                                    "query": queryString,
                                    "type": "cross_fields",
                                    "default_operator": "OR",
                                    "minimum_should_match": "3<90%",
                                    "fields": [
                                        "title^2",
                                        "*"
                                    ],
                                    "analyze_wildcard": true,
                                    "boost": 1
                                }
                            },
                            {
                                "query_string": {
                                    "query": queryString,
                                    "type": "cross_fields",
                                    "minimum_should_match": "50%",
                                    "default_operator": "OR",
                                    "fields": [
                                        "title^2",
                                        "*"
                                    ],
                                    "analyze_wildcard": true,
                                    "boost": 0.01
                                }
                            }
                        ],
                        "must": []
                    }
                },
                "highlight": {
                    "fields": {
                      "*": { "pre_tags" : ["<b class='highlighted-text'>"], "post_tags" : ["</b>"] }
                    }
                }
            }
        }
    } else {
        let queryStringArray = queryString.split(" ");
        queryString = '';
        for(arrayString of queryStringArray){
            if(arrayString != ''){
                queryString += arrayString + "~2 ";
            }
        }
        queryBody = {
            index: indexString,
            body: {
                "size": PAGE_SIZE, "from": PAGE_SIZE * (page - 1),
                "query": {
                    "bool": {
                        "should": [
                            {
                                "query_string": {
                                    "query": queryString,
                                    "type": "best_fields",
                                    "phrase_slop": 0,
                                    "default_operator": "AND",
                                    "fields": [
                                        "title^5",
                                        "*"
                                    ],
                                    "analyze_wildcard": true,
                                    "boost": 2
                                }
                            },
                            {
                                "query_string": {
                                    "query": queryString,
                                    "type": "best_fields",
                                    "default_operator": "AND",
                                    "fields": [
                                        "title^5",
                                        "*"
                                    ],
                                    "analyze_wildcard": true,
                                    "boost": 1.5
                                }
                            },
                            {
                                "query_string": {
                                    "query": queryString,
                                    "type": "cross_fields",
                                    "default_operator": "OR",
                                    "minimum_should_match": "3<90%",
                                    "fields": [
                                        "title^2",
                                        "*"
                                    ],
                                    "analyze_wildcard": true,
                                    "boost": 1
                                }
                            },
                            {
                                "query_string": {
                                    "query": queryString,
                                    "type": "cross_fields",
                                    "minimum_should_match": "50%",
                                    "default_operator": "OR",
                                    "fields": [
                                        "title^2",
                                        "*"
                                    ],
                                    "analyze_wildcard": true,
                                    "boost": 0.01
                                }
                            }
                        ],
                        "must": []
                    }
                },
                "highlight": {
                    "fields": {
                      "*": { "pre_tags" : ["<b class='highlighted-text'>"], "post_tags" : ["</b>"] }
                    }
                }
            }
        }
    }

    if(contentTypeFilter){
        queryBody["body"]["query"]["bool"]["filter"] = [{ "match": { "contentType": contentTypeFilter }}];
    }
    
    applyFiltersToQuery(queryBody, filters);
    return (await elasticClient.search(queryBody));
}

exports.simpleQueryTypes = async(elasticClient, queryString) => {
    const queryBody = {
        index: indexString,
        body: {
            "query": {
                "bool": {
                    "must": [
                        { "query_string": {"query": queryString} }
                    ]
                }
            }
        }
    }
    return (await elasticClient.search(queryBody));
}

exports.simpleQueryFilterOptions = async(elasticClient, queryString) => {
    const queryBody = {
        index: indexString,
        body: {
            "query": {
                "bool": {
                    "must": [
                        { "query_string": {"query": queryString} }
                    ]
                }
            },
            "aggs": {
                "source_agg": {
                    "terms": {
                        "field": "source",
                        "size": 50
                    }
                }
            }
        }
    }
    return (await elasticClient.search(queryBody));
}

exports.simpleQueryDataDictionary = async(elasticClient, queryString) => {
    const queryBody = {
        index: dataDictionaryIndexString,
        body: {
            "query": {
                "bool": {
                    "must": [
                        {
                            "query_string": {
                                "query": queryString,
                                "default_operator": "AND"
                            }
                        }
                    ]
                }
            }
        }
    }
    return (await elasticClient.search(queryBody));
}

exports.addClickLog = async(elasticClient, queryString) => {
    var filters = queryString.filters;
    var filtersArray = [];
    filtersArray.push({"filter_field": "start_date", "filter_value": filters.startDate});
    filtersArray.push({"filter_field": "end_date", "filter_value": filters.endDate});
    filtersArray.push({"filter_field": "all_dates", "filter_value": filters.allDates});
    filtersArray.push({"filter_field": "search_order", "filter_value": filters.searchOrder});

    if(filters.checkBoxFilters){
        filters.checkBoxFilters.forEach(checkBoxFilter => {
            checkBoxFilter.values.forEach(filterValue => {
                filtersArray.push({"filter_field": checkBoxFilter.name, "filter_value": filterValue});
            });
        });
    }
    
    const queryBody = {
        index: "c205-web-analytics",
        body: {
            "@timestamp": new Date(queryString.detail_click_time),
            "details_click_through_order": queryString.details_click_through_order,
            "document_id": queryString.document_id,
            "external_click_through": queryString.external_click_through,
            "search_result_ranking": queryString.result_rank,
            "search_timestamp": new Date(queryString.search_time),
            "user_id": queryString.user_id,
            "search_term": queryString.search_term,
            "filters": filtersArray,
            "index_name": queryString.index_name,
            "feedback_response": {
                "relevant": queryString.feedbackResponse.relevant
            },
        }
    };
    return (await elasticClient.index(queryBody));
}

exports.addSearchLog = async(elasticClient, userid, queryString, pageNum, searchResults) => {
    var searchResultsReformatted = [];
    
    searchResults.forEach(element => {
        searchResultsReformatted.push({
            "id": element._id,
            "index": element._index,
        });
    });

    const queryBody = {
        index: "c205-web-logs",
        body: {
            "@timestamp": new Date(),
            "userID": userid,
            "searchTerm": queryString,
            "page_num": pageNum,
            "searchResults": searchResultsReformatted,
        }
    };

    return (await elasticClient.index(queryBody));
}

exports.idLookup = async(elasticClient, id) => {
    return (await elasticClient.search({
        index: indexString,
        body: {
            "query": {
                "terms": {
                    "_id": [id]
                }
            }
        }
    }))
}

function applyFiltersToQuery(queryBody, filters){
    if(filters){
        switch(filters.searchOrder){
            case 1:
                break;
            case 2:
                queryBody["body"]["sort"] = [{"coverage_start_date": {"order": "desc", "unmapped_type" : "long"}}]
                break;
            case 3:
                queryBody["body"]["sort"] = [{"coverage_start_date": {"order": "asc", "unmapped_type" : "long"}}]
                break;
            default:
                break;
        }
        
        if(filters.checkBoxFilters && filters.checkBoxFilters.length > 0){
            queryBody["body"]["query"]["bool"]["filter"] = [];
            filters.checkBoxFilters.forEach(function(item){
                const keyValue = {};
                keyValue[item.name] = item.values;
                queryBody["body"]["query"]["bool"]["filter"].push({"terms": keyValue});
                queryBody["body"]["query"]["bool"]["minimum_should_match"] = 1
            });
        }
        
        if(filters.allDates == false){
            const rangeFilter = {"range": {"coverage_start_date": { "gte": filters.startDate, "lte": filters.endDate}}};
            
            queryBody["body"]["query"]["bool"]["must"].push(rangeFilter);
        }
    }
}