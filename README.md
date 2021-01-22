# aws-chalice
In order to get started using AWS Chalice we need to install/configure the following requirements:
* Python 3.7
* Virtualenv
* AWS credentials
* AWS CLI
* boto3
* git

This is a simple workshop step by step and the intention is to reproduce the follow arquitecture by building a very simple and uncomplete ToDo APP.
![alt text](https://github.com/stahlmatias/aws-chalice/blob/main/img/Secure-API-Gateway.png?raw=true)

1. Deploy todo-table
```
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
```
3. Copy app.py and .chalice directory
4. Deploying the app
