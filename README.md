<!--
title: 'Serverless Framework Python Flask API on AWS'
description: 'This template demonstrates how to develop and deploy a simple Python Flask API running on AWS Lambda using the traditional Serverless Framework.'
layout: Doc
framework: v3
platform: AWS
language: Python
priority: 2
authorLink: 'https://github.com/serverless'
authorName: 'Serverless, inc.'
authorAvatar: 'https://avatars1.githubusercontent.com/u/13742415?s=200&v=4'
-->

# Serverless Google Workspace API

### Deploy

Before deploying:

1. Create a .env file locally from `.env.example`
2. Set `GOOGLE_WORKSPACE_SERVICE_ACCOUNT_CREDENTIALS` with the service credentials JSON
3. Set `GOOGLE_WORKSPACE_SERVICE_ACCOUNT_DELEGATED_USER` with the admin user acting as delegate
4. Set `GOOGLE_WORKSPACE_CUSTOMER_ID` with the Google Workspace Customer ID
5. Deploy:


    just deploy

After initial deploy, add the Queue Event trigger to your S3 Bucket

### Development

Install pipenv and activate environment

    pipenv shell

Install serverless node environment (note this environment has shortcomings because of lack of SQS support)

    npm install
    just start

### Test

Run unit tests with a simple `justfile` command

    just test

### Production

    just stage=production deploy
