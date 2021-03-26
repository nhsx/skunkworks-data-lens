# DataLens-Semantic

Project for document vectorisation and semantic querying of NHSx datasets

## Requirements

- Docker
- Docker Compose >= [1.22.0](https://docs.docker.com/compose/release-notes/#1220)

## Getting Started

### 1. Download a pretrained BioBERT model

The bioBERT model files will likely have the prefix: biobert_model*
This needs to be changed to just: bert_model* for now.

### 2. Set environment variables

PATH_MODEL: the folder containing the model

DATALENS_CONFIG: the config directory (containing sources.json)

ELASTICSEARCH_ADDRESS: the URL and port of the elastic cluster

DATALENS_SEARCH_SIZE: how many documents to return from each elastic search

DATALENS_MINIMUM_ZSCORE: The minimum z-score a search result should have in order to be valid

### 3. Docker compose

Run docker-compose up --build

(You can neglect build if there have been no changes to the repo since last build.)

### 4. Swagger page

Go to http://127.0.0.1/

## Deployment

### 1. Pushing the Docker image

```
aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin {server_id}.dkr.ecr.eu-west-2.amazonaws.com

docker tag datalens-semantic_web:latest {server_id}.dkr.ecr.eu-west-2.amazonaws.com/datalens-semantic_web:latest

docker push {server_id}.dkr.ecr.eu-west-2.amazonaws.com/datalens-semantic_web:latest
```

### 2. Kill the ECS tasks

Cluster: datalens-semantic

Service: datalens-semantic-service

This will cause the ECS to pull the latest docker image from the ECR above.

### 3. Task definition changes

In deploy/ there is the latest task definition, including setting of environment variables. Keep this up to date. If you know which changes you want to make to it, you can use it as a source for creating new revisions to the task definition.
