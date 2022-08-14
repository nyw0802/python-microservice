import boto3
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# dynamodb tb connection
dynamoTable = "node"
dynamo = boto3.resource('dynamodb')
table = dynamo.Table(dynamoTable)


def lambda_handler(event, context):
    logger.info(event)
    # httpMethod
    httpMethod = event['httpMethod']

    # save - POST
    if httpMethod == 'POST':
        requestbody = json.loads(event['body'])
        response = saveNode(requestbody)
        logger.info(response)

    # get - GET
    if httpMethod == 'GET' and event['queryStringParameters']['nodeId']:
        response = getNode(event['queryStringParameters']['nodeId'])
        logger.info(response)

    # delete - DELETE
    if httpMethod == 'DELETE' and event['queryStringParameters']['nodeId']:
        response = deleteNode(event['queryStringParameters']['nodeId'])
        logger.info(response)

    return response


def deleteNode(nodeId):
    response = table.delete_item(
        Key={
            'nodeId': nodeId
        }
    )
    body = {
        'operation': 'DELETE',
        'message': 'SUCCESS',
        'Iteam': nodeId
    }
    return buildResponse(200, body)


def saveNode(requestbody):
    try:
        table.put_item(Item=requestbody)
        body = {
            'operation': 'SAVE',
            'message': 'SUCCESS',
            'Item': requestbody
        }
        return buildResponse(200, body)
    except:
        logger.exception('handle error here...')


def getNode(nodeId):
    response = table.get_item(
        Key={
            'nodeId': nodeId
        }
    )
    if 'Item' in response:
        return buildResponse(200, response['Item'])
    else:
        return buildResponse(200, {'Message': 'node id %s is not found' % nodeId})


def buildResponse(statusCode, body=None):
    response = {
        'statusCode': statusCode,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-All-Origin': '*'
        }
    }
    if body is not None:
        response['body'] = json.dumps(body)

    return response
