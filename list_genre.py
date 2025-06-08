import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('genres')

def lambda_handler(event, context):
    if event.get("httpMethod") == "GET" and event.get("path") == "/genres":
        try:
            response = table.scan()
            genres = response.get("Items", [])

            return {
                "statusCode": 200,
                "body": json.dumps(genres),
                "headers": {"Content-Type": "application/json"}
            }

        except ClientError as e:
            return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

    return {"statusCode": 404, "body": json.dumps({"error": "Route not found"})}
