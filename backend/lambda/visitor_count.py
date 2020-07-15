import boto3
import json
import os


def lambda_handler(event, context):
    # Init DynamoDB Client
    dynamodb = boto3.resource("dynamodb")
    # Set dynamodb table name variable from env
    ddbTableName = os.environ["databaseName"]
    table = dynamodb.Table(ddbTableName)
    # table = dynamodb.Table("tvq-cloud-resume-counter")

    # Atomic update item in table or add if doesn't exist
    ddbResponse = table.update_item(
        Key={"id": "visitorCount"},
        UpdateExpression="ADD amount :inc",
        ExpressionAttributeValues={":inc": 1},
        ReturnValues="UPDATED_NEW",
    )

    # Format dynamodb response into variable
    responseBody = json.dumps(
        {"visitorCount": int(float(ddbResponse["Attributes"]["amount"]))}
    )

    # Create api response object
    apiResponse = {
        "isBase64Encoded": False,
        "statusCode": 200,
        "body": responseBody,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,x-requested-with",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,OPTIONS",
        },
    }

    return apiResponse
