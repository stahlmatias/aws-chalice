from chalice import Chalice
from chalice import CustomAuthorizer
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

app = Chalice(app_name='todo-app')
app.debug = True
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table('todo-table')

authorizer = CustomAuthorizer(
    'MyCustomAuth', ttl_seconds=10, header='Authorization',
    authorizer_uri=('arn:aws:apigateway:us-east-1:lambda:path/2015-03-31'
                    '/functions/arn:aws:lambda:us-east-1:298890264621:'
                    'function:GetStartedLambdaIntegrationAuthorizer/invocations'))


@app.route('/getTodo/{id}', methods=['GET'], authorizer=authorizer)
def get_todo(id):
    username = app.current_request.context["authorizer"]["principalId"]
    try:
        response = table.get_item(Key={'id': id, 'username': username})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Item']


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


@app.route('/updateTodo', methods=['PUT'], authorizer=authorizer)
def update_todo():
    username = app.current_request.context["authorizer"]["principalId"]
    body = app.current_request.json_body
    response = table.update_item(
        Key={
            'id': body.get('id'),
            'username': username
        },
        UpdateExpression="set completed = :c, task =:t",
        ExpressionAttributeValues={
            ':t': body.get('task'),
            ':c': body.get('completed')
        },
        ReturnValues="UPDATED_NEW"
    )
    return response


@app.route('/getAllTodo', methods=['GET'], authorizer=authorizer)
def get_all_todo():
    username = app.current_request.context["authorizer"]["principalId"]
    response = table.query(
        KeyConditionExpression=Key('username').eq(username)
    )
    return response['Items']
