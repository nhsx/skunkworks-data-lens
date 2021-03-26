const { query } = require('express');
const fetch = require('node-fetch');
const url = "http://datalens-semantic-alb-967737509.eu-west-2.elb.amazonaws.com/semantic/";

exports.getSearchAndFilterResults = async (queryString) => {
    return fetch(url + "search-and-filter?query=" + queryString)
        .then(res => res.json())
        .then(data => {
            return data;
        })
        .catch(err => {
            console.log(err);
        });
}

exports.getRecommendations = async (indexString, idString) => {
    return fetch(url + "recommendations?index=" + indexString + "&ID=" + idString)
        .then(res => res.json())
        .then(data => {
            return data;
        })
        .catch(err => {
            console.log(err);
        });
}
