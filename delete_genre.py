import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('genres')

def lambda_handler(event, context):
    if event.get("httpMethod") == "DELETE" and event.get("path") == "/genres":
        data = json.loads(event.get("body", "{}"))
        genre_id = data.get("genre_id")

        if not genre_id:
            return {"statusCode": 400, "body": json.dumps({"error": "Genre ID is required"})}

        table.delete_item(Key={"genre_id": genre_id})

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Genre deleted"}),
            "headers": {"Content-Type": "application/json"}
        }

    return {"statusCode": 404, "body": json.dumps({"error": "Route not found"})}
