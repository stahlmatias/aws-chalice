# aws-chalice

Chalice's API for writing serverless application uses a familiar decorator-based syntax used in frameworks such as Flask, bottle, and FastAPI.  Chalice automatically determines how to provision the necessary resources for your application. Chalice lets you quickly create and deploy python applications that use AWS Lambda. Using the Chalice CLI, you can have a REST API deployed to Amazon API Gateway and AWS Lambda in minutes. 

This workshop will walk through creating a serverless web API to update, get a Todo’s, managing Todo’s in a database, adding authorization with JWT, and creating a full CI/CD pipeline for the application. 

AWS services covered include AWS Lambda, Amazon API Gateway, Amazon DynamoDB, AWS CodeBuild, and AWS CodePipeline.

In order to get started using AWS Chalice we need to install/configure the following requirements:
* Python 3.7
* Virtualenv
* AWS credentials
* AWS CLI
* boto3
* git

This is a simple workshop step by step and the intention is to reproduce the following arquitecture by building a very simple and (un)complete ToDo APP. We are going to focus in the development of the API Gateway Resoure by using AWS Chalice.

![alt text](https://github.com/stahlmatias/aws-chalice/blob/main/img/Secure-API-Gateway.png?raw=true)

## Simple (uncomplete) ToDo App
![alt text](https://github.com/stahlmatias/aws-chalice/blob/main/img/AWS-Chalice.png?raw=true)


1. Deploy todo-table
```
$ cat dynamodb_cf.yaml 
AWSTemplateFormatVersion: '2010-09-09'
Metadata:
  License: Apache-2.0
Description: 'AWS CloudFormation Sample Template DynamoDB_Table: This template demonstrates
  the creation of a DynamoDB table.  **WARNING** This template creates an Amazon DynamoDB
  table. You will be billed for the AWS resources used if you create a stack from
  this template.'
Resources:
  todoTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: todo-table
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: id
          AttributeType: S
        - AttributeName: username
          AttributeType: S
      KeySchema:
        - AttributeName: username
          KeyType: HASH
        - AttributeName: id
          KeyType: RANGE
Outputs:
  TableName:
    Value: !Ref 'todoTable'
    Description: Table name of the newly created DynamoDB table

$ aws cloudformation deploy \ 
 --template-file dynamodb_cf.yaml \
 --stack-name "todo-stack"
 ```

2. Create a new chalice project
``` 
$ python3 -m venv aws-chalice-env
$ source aws-chalice-env/bin/activate
$ pip install chalice
$ chalice new-project aws-chalice
$ cd aws-chalice
```

3. Copy app.py and .chalice directory
```
aws-chalice $ tree -a
.
├── .chalice
│   ├── config.json
│   └── policy-dev.json
├── app.py
├── requirements.txt
```

4. Deploying the app
```
$ chalice deploy
Creating deployment package.
Creating IAM role: aws-chalice-dev
Creating lambda function: aws-chalice-dev
Creating Rest API
Resources deployed:
  - Lambda ARN: arn:aws:lambda:us-west-2:12345:function:aws-chalice-dev
  - Rest API URL: https://1y2mueb824.execute-api.us-east-1.amazonaws.com/api/
```

## Verification
```
$ aws dynamodb scan --table-name todo-table
{
    "Items": [
        {
            "completed": {
                "S": "uncompleted"
            },
            "task": {
                "S": "task 1"
            },
            "username": {
                "S": "matias"
            },
            "id": {
                "S": "1"
            }
        },
        {
            "completed": {
                "S": "completed"
            },
            "task": {
                "S": "task 1"
            },
            "username": {
                "S": "authlete_16447040290054"
            },
            "id": {
                "S": "1"
            }
        },
        {
            "completed": {
                "S": "uncompleted"
            },
            "task": {
                "S": "task 2"
            },
            "username": {
                "S": "authlete_16447040290054"
            },
            "id": {
                "S": "2"
            }
        },
        {
            "completed": {
                "S": "uncompleted"
            },
            "task": {
                "S": "task 3"
            },
            "username": {
                "S": "authlete_16447040290054"
            },
            "id": {
                "S": "3"
            }
        }
    ],
    "Count": 4,
    "ScannedCount": 4,
    "ConsumedCapacity": null
}

```

###### /updateTodo
```
$ echo '{"id":"1", "task": "new task 1", "completed": "uncompleted"}' | http PUT https://z2f3y3lib6.execute-api.us-east-1.amazonaws.com/api/updateTodo/
HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 455
Content-Type: application/json
Date: Tue, 19 Jan 2021 19:48:26 GMT
Via: 1.1 4e6914a651880fafa65640c6561ae2a8.cloudfront.net (CloudFront)
X-Amz-Cf-Id: dGKZ39ATrZHqXME1NSaadoRGfuccZQ0XVEpVRnQaB-v87puHLCW_Aw==
X-Amz-Cf-Pop: EZE51-C1
X-Amzn-Trace-Id: Root=1-6007378a-41818d1166d9fdb81ad25f51;Sampled=0
X-Cache: Miss from cloudfront
x-amz-apigw-id: ZaWdoEdOoAMFwUQ=
x-amzn-RequestId: cd43edac-04da-4828-85d8-98916b4fda62

{
    "Attributes": {
        "completed": "uncompleted",
        "task": "new task 1"
    },
    "ResponseMetadata": {
        "HTTPHeaders": {
            "connection": "keep-alive",
            "content-length": "74",
            "content-type": "application/x-amz-json-1.0",
            "date": "Tue, 19 Jan 2021 19:48:26 GMT",
            "server": "Server",
            "x-amz-crc32": "1632463437",
            "x-amzn-requestid": "9UDMNTCUDM3S221UON8RNUJPF3VV4KQNSO5AEMVJF66Q9ASUAAJG"
        },
        "HTTPStatusCode": 200,
        "RequestId": "9UDMNTCUDM3S221UON8RNUJPF3VV4KQNSO5AEMVJF66Q9ASUAAJG",
        "RetryAttempts": 0
    }
}
```

###### /completeTodo/{id}
```
$ curl -X GET 'https://z2f3y3lib6.execute-api.us-east-1.amazonaws.com/api/completeTodo/1' \
-H 'Authorization: Bearer L66krSgrqLtUDrjhL3-culTysBCxci-WBIZeJNE8EZo'

{
   "Attributes":{
      "completed":"completed"
   },
   "ResponseMetadata":{
      "RequestId":"L07ID7VARALOVIJ141OHUS147VVV4KQNSO5AEMVJF66Q9ASUAAJG",
      "HTTPStatusCode":200,
      "HTTPHeaders":{
         "server":"Server",
         "date":"Fri, 22 Jan 2021 19:02:22 GMT",
         "content-type":"application/x-amz-json-1.0",
         "content-length":"46",
         "connection":"keep-alive",
         "x-amzn-requestid":"L07ID7VARALOVIJ141OHUS147VVV4KQNSO5AEMVJF66Q9ASUAAJG",
         "x-amz-crc32":"3307285739"
      },
      "RetryAttempts":0
 
```
###### /getAllTodo
```
$ curl -X GET 'https://z2f3y3lib6.execute-api.us-east-1.amazonaws.com/api/getAllTodo' \ 
 -H 'Authorization: Bearer L66krSgrqLtUDrjhL3-culTysBCxci-WBIZeJNE8EZo'
[
   {
      "completed":"completed",
      "task":"new task 1",
      "username":"authlete_16447040290054",
      "id":"1"
   },
   {
      "completed":"uncompleted",
      "task":"task 2",
      "username":"authlete_16447040290054",
      "id":"2"
   },
   {
      "completed":"uncompleted",
      "task":"task 3",
      "username":"authlete_16447040290054",
      "id":"3"
   }
]
```

# AWS Lambda authorizers with a third-party identity provider

Chalice supports multiple mechanisms for authorization. Here I will show you how you can integrate authorization into your Chalice applications.

In Chalice, all the authorizers are configured per-route and specified using the authorizer kwarg to an @app.route() call. You control which type of authorizer to use based on what’s passed as the authorizer kwarg. You can use the same authorizer instance for multiple routes.

API Gateway also lets you write custom authorizers using a Lambda function. You can configure a Chalice route to use a pre-existing Lambda function as a custom authorizer.

```
from chalice import CustomAuthorizer

authorizer = CustomAuthorizer(
    'MyCustomAuth', ttl_seconds=10, header='Authorization',
    authorizer_uri=('arn:aws:apigateway:us-east-1:lambda:path/2015-03-31'
                    '/functions/arn:aws:lambda:us-east-1:298890264621:'
                    'function:GetStartedLambdaIntegrationAuthorizer/invocations'))

@app.route('/completeTodo/{id}', methods=['GET'], authorizer=authorizer)
def complete_todo(id):
    username = app.current_request.context["authorizer"]["principalId"]
    response = table.update_item(
        Key={
            'id': id,
            'username': username
        },
        UpdateExpression="set completed = :c",
        ExpressionAttributeValues={
            ':c': "completed"
        },
        ReturnValues="UPDATED_NEW"
    )
    return response
```
# Create a SAM template
With this simple command you can create a SAM Template for this app.

```
$ chalice package packaged/
$ tree packaged/
packaged/
├── deployment.zip
└── sam.json

```
# Deploy your SAM template
1. cd to the packaged directory
```
$ cd packaged/
$ ls -la
.
..
deployment.zip
sam.json
```

2. Create an Amazon S3 bucket in order to deploy the app using CloudFormation
```
$ aws s3 mb s3://chalice-teco-cfn-bucket/ --region us-east-1
```

3. Upload your code to the S3 bucket and create a new SAM template that references your S3 object. 
```
$ aws cloudformation package --template-file ./packaged/sam.json \
--s3-bucket chalice-teco-cfn-bucket --output-template-file sam-packaged.yaml
```
4. Deploy your application using the AWS CLI
```
$ aws cloudformation deploy --template-file ./sam-packaged.yaml \
    --stack-name chalice-teco-beta-stack \
    --capabilities CAPABILITY_IAM
```
5. Verification
```
$ aws cloudformation describe-stacks --stack-name chalice-teco-beta-stack \
--query 'Stacks[0].StackStatus'
"CREATE_COMPLETE"
```

6. Get the endpoint URL
```
$ aws cloudformation describe-stacks --stack-name chalice-teco-beta-stack \
>     --query 'Stacks[0].Outputs'
[
    {
        "OutputKey": "APIHandlerArn",
        "OutputValue": "arn:aws:lambda:us-east-1:298890264621:function:chalice-teco-beta-stack-APIHandler-15E55I1QPQFXA"
    },
    {
        "OutputKey": "APIHandlerName",
        "OutputValue": "chalice-teco-beta-stack-APIHandler-15E55I1QPQFXA"
    },
    {
        "OutputKey": "RestAPIId",
        "OutputValue": "us3zhe4t7j"
    },
    {
        "OutputKey": "EndpointURL",
        "OutputValue": "https://us3zhe4t7j.execute-api.us-east-1.amazonaws.com/api/"
    }
]
```
7. Test the api
```
$ curl -X GET 'https://us3zhe4t7j.execute-api.us-east-1.amazonaws.com/api/getAllTodo' \
-H 'Authorization: Bearer T12FKRqCPCChaQaYRY1qBZA_h1oWXOwTZ-MGLsmAwTk'
[
   {
      "completed": "completed",
      "task": "new task 1",
      "username": "authlete_16447040290054",
      "id": "1"
   },
   {
      "completed": "uncompleted",
      "task": "task 2",
      "username": "authlete_16447040290054",
      "id": "2"
   },
   {
      "completed": "uncompleted",
      "task": "task 3",
      "username": "authlete_16447040290054",
      "id": "3"
   }
]
```
# Implement observability best practices

The first thing we need to do is import the appropriate packages then instantiate these classes and next register middleware for our application.

```
from chalice import Chalice
from chalice.app import ConvertToMiddleware

import requests
from aws_lambda_powertools import Logger
from aws_lambda_powertools import Tracer

logger = Logger()
tracer = Tracer()
session = requests.Session()

app.register_middleware(ConvertToMiddleware(logger.inject_lambda_context))
app.register_middleware(ConvertToMiddleware(tracer.capture_lambda_handler))


@app.middleware('http')
def inject_route_info(event, get_response):
    logger.structure_logs(append=True, request_path=event.path)
    return get_response(event)
```

The `inject_route_info` middleware is registered to any Lambda functions associated with our HTTP API, and will automatically be invoked before every view function is called.

Before we can deploy our code, we need to ensure our application is configured appropriately. To do this, update your .chalice/config.json file to enable AWS X-Ray as well as set the service name for your app by creating a POWERTOOLS_SERVICE_NAME environment variable.

```
{
  "version": "2.0",
  "app_name": "todo-app",
  "xray": true,
  "environment_variables": {
    "POWERTOOLS_SERVICE_NAME": "middleware-demo"
  },
  "stages": {
    "dev": {
      "autogen_policy": false,
      "api_gateway_stage": "api"
    }
  }
}
```

# Working with AWS CodePipeline

## Creating a pipeline

1. Create a release/ directory.
```
$ mkdir release/
```
2. Generate a CloudFormation template for the starter CD pipeline
```
$ chalice generate-pipeline --pipeline-version v2 release/pipeline.json
```
3. Deploy this template using the AWS CLI
```
$ aws cloudformation deploy --stack-name chalice-teco-pipeline-stack \
    --template-file release/pipeline.json \
    --capabilities CAPABILITY_IAM
```
4. Initialize the app as a git repository
```
$ git init .
```
5. Commit your existing files
```
$ git add -A .
$ git commit -m "Initial commit"
```
6. Query the CloudFormation stack
```
$ aws cloudformation describe-stacks     --stack-name chalice-teco-pipeline-stack     --query 'Stacks[0].Outputs'
[
    {
        "OutputKey": "CodeBuildRoleArn",
        "OutputValue": "arn:aws:iam::298890264621:role/chalice-teco-pipeline-stack-CodeBuildRole-OCI8ZFIFMUSV"
    },
    {
        "OutputKey": "CFNDeployRoleArn",
        "OutputValue": "arn:aws:iam::298890264621:role/chalice-teco-pipeline-stack-CFNDeployRole-1HHEPMVZ5YJ5W"
    },
    {
        "OutputKey": "S3ApplicationBucket",
        "OutputValue": "chalice-teco-pipeline-stack-applicationbucket-v6rxjiacf03i"
    },
    {
        "OutputKey": "CodePipelineRoleArn",
        "OutputValue": "arn:aws:iam::298890264621:role/chalice-teco-pipeline-stack-CodePipelineRole-1862VZ6FAIEBA"
    },
    {
        "OutputKey": "SourceRepoURL",
        "OutputValue": "https://git-codecommit.us-east-1.amazonaws.com/v1/repos/aws-chalice-test"
    },
    {
        "OutputKey": "S3PipelineBucket",
        "OutputValue": "chalice-teco-pipeline-stack-artifactbucketstore-1sep3wgf6mwkw"
    }
]

```
7. Copy the value for the SourceRepoURL and configure a new git remote named codecommit
```
$ git remote add codecommit https://git-codecommit.us-east-1.amazonaws.com/v1/repos/aws-chalice-test
```

8. Configure the CodeCommit credential helper. Append these lines to the end of your .git/config file
```
[credential]
    helper =
    helper = !aws codecommit credential-helper $@
    UseHttpPath = true
```
9. Verify you have a codecommit remote

```
$ git remote -v
codecommit	https://git-codecommit.us-east-1.amazonaws.com/v1/repos/aws-chalice-test (fetch)
codecommit	https://git-codecommit.us-east-1.amazonaws.com/v1/repos/aws-chalice-test (push)

```
10. Pushing changes to AWS CodeCommit
```
$ git add -A .
$ git commit -m "modifying buildspec"
$ git push codecommit master
Enumerating objects: 7, done.
Counting objects: 100% (7/7), done.
Delta compression using up to 4 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (4/4), 517 bytes | 517.00 KiB/s, done.
Total 4 (delta 2), reused 0 (delta 0)
To https://git-codecommit.us-east-1.amazonaws.com/v1/repos/aws-chalice-test
   3ecfb85..fb86030  master -> master

```
## Verification
The best way to verify the pipeline is working as expected is to view the pipeline in the console and wait until the stages have completed and all the stages are green.

![alt text](https://github.com/stahlmatias/aws-chalice/blob/main/img/CodePipeline.png?raw=true)

![alt text](https://github.com/stahlmatias/aws-chalice/blob/main/img/CodePipelineII.png?raw=true)


# Resources
[AWS Chalice A framework for writing serverless applications](https://aws.github.io/chalice/index.html)

[Introducing custom authorizers in Amazon API Gateway](https://aws.amazon.com/blogs/compute/introducing-custom-authorizers-in-amazon-api-gateway/)

[Authlete Amazon API Gateway + Custom Authorizer + OAuth](https://www.authlete.com/developers/custom_authorizer/)

[Following serverless best practices with AWS Chalice and Lambda Powertools](https://aws.amazon.com/blogs/developer/following-serverless-best-practices-with-aws-chalice-and-lambda-powertools/)
