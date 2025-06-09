import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('vibes')

def lambda_handler(event, context):
    response = table.get_item(Key={"id": "123"})
    item = response.get("Item", {})
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Hello there."})
    }
