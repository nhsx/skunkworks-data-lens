const {getElasticClient} = require('../services/elasticsearch');

function createElasticClient(req, res, next) {
    if(process.env.BYPASS_AUTH == "true"){
        req.elasticClient = getElasticClient(process.env.ELASTIC_USERNAME);
    }
    else {
        if(req.user.nameID){
            req.elasticClient = getElasticClient(req.user.nameID);
        }
        else {
            req.elasticClient = getElasticClient(req.session.passport.user.cn);
        }
    }
    next();
}

exports.createElasticClient = createElasticClient;