const express = require('express');

// Configuration
const { SERVER_PORT, STAGING_PORT } = require('./config')
const configureAPI = require('./configure');
const passportConfigure = require('./passportConfigure');
require('dotenv').config()

const queryRouter = require('./routers/queryRouter');
const authMiddleware = require('./middleware/authMiddleware');
const elasticClientMiddleware = require("./middleware/elasticClientMiddleware");

const app = express();

configureAPI(app);
passportConfigure(app);

if(process.env.BYPASS_AUTH !== "true"){
    app.use(authMiddleware);
}

app.use(elasticClientMiddleware.createElasticClient);

app.use(`/api`, queryRouter);

if (process.env.NODE_ENV == "staging")
{
    console.log(process.env.NODE_ENV)
    app.listen(STAGING_PORT, () => console.log(`Server running on port ${STAGING_PORT}`));
}
else 
{
    console.log(process.env.NODE_ENV)
    app.listen(SERVER_PORT, () => console.log(`Server running on port ${SERVER_PORT}`));
}

