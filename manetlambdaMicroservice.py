import boto3
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# dynamodb tb connection
dynamoTable = "MANET"
dynamo = boto3.resource('dynamodb')
table = dynamo.Table(dynamoTable)


def lambda_handler(event, context):
    logger.info(event)
    # httpMethod
    httpMethod = event['httpMethod']

    # save - POST
    if httpMethod == 'POST':
        requestbody = json.loads(event['body'])
        response = saveMANET(requestbody)
        logger.info(response)

    # get - GET
    if httpMethod == 'GET' and event['queryStringParameters']['manetId']:
        response = getMANET(event['queryStringParameters']['manetId'])
        logger.info(response)

    # delete - DELETE
    if httpMethod == 'DELETE' and event['queryStringParameters']['manetId']:
        response = deleteMANET(event['queryStringParameters']['manetId'])
        logger.info(response)

    return response


def deleteMANET(manetId):
    response = table.delete_item(
        Key={
            'manetId': manetId
        }
    )
    body = {
        'operation': 'DELETE',
        'message': 'SUCCESS',
        'Iteam': manetId
    }
    return buildResponse(200, body)


def saveMANET(requestbody):
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


def getMANET(manetId):
    response = table.get_item(
        Key={
            'manetId': manetId
        }
    )
    if 'Item' in response:
        return buildResponse(200, response['Item'])
    else:
        return buildResponse(200, {'Message': 'manet id %s is not found' % manetId})


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
