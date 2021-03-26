export default {
    buildCommsCallLogQuery(sourceNumber, recipientNumber, time){
        return {
            "query": {
                "function_score": {
                    "functions": [
                        {
                            "linear": {
                                "event_time": {
                                    "origin": time,
                                    "scale": "28800m"
                                }
                            }
                        }
                    ],
                    "score_mode": "multiply",
                    "boost_mode": "multiply",
                    "query": {
                        "bool": {
                            "should": [
                                {
                                    "bool": {
                                        "must": [
                                            {
                                                "term": {
                                                    "call_source_number.keyword": sourceNumber
                                                }
                                            },
                                            {
                                                "term": {
                                                    "call_recipient_number.keyword": recipientNumber
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    "bool": {
                                        "must": [
                                            {
                                                "term": {
                                                    "call_source_number.keyword": recipientNumber
                                                }
                                            },
                                            {
                                                "term": {
                                                    "call_recipient_number.keyword": sourceNumber
                                                }
                                            }
                                        ]
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        }
    }
}