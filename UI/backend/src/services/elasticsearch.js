const { Client } = require('@elastic/elasticsearch')

const elasticUrl = process.env.ELASTIC_URL || "https://localhost:9200";

function getElasticClient(runAsUser){
    return new Client({
        node: {
            url: new URL(elasticUrl),
            headers: {
                "es-security-runas-user": runAsUser,
            },
            auth: {
                username: process.env.ELASTIC_USERNAME,
                password: process.env.ELASTIC_PASSWORD
            }
        }
    });
};


exports.getElasticClient = getElasticClient;