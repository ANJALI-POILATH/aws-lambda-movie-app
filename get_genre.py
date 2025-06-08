import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('genres')

def lambda_handler(event, context):
    if event.get("httpMethod") == "GET" and event.get("path") == "/genre":
        genre_id = event.get("queryStringParameters", {}).get("genre_id")

        if not genre_id:
            return {"statusCode": 400, "body": json.dumps({"error": "genre_id is required"})}

        try:
            response = table.get_item(Key={"genre_id": genre_id})
            genre = response.get("Item")

            if not genre:
                return {"statusCode": 404, "body": json.dumps({"error": "Genre not found"})}

            return {
                "statusCode": 200,
                "body": json.dumps(genre),
                "headers": {"Content-Type": "application/json"}
            }

        except ClientError as e:
            return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

    return {"statusCode": 404, "body": json.dumps({"error": "Route not found"})}
