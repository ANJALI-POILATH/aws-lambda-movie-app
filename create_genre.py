import json
import boto3
import uuid
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table = dynamodb.Table('genres')

def lambda_handler(event, context):
    if event.get("httpMethod") == "POST" and event.get("path") == "/genres":
        try:
            body = json.loads(event.get("body", "{}"))
            genre_name = body.get("genre_name")
            movie_id = body.get("id")  # Optional reference to a movie UUID

            if not genre_name:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": "genre_name is required"})
                }

            # 🔗 UUID auto-generated for genre
            genre_id = str(uuid.uuid4())

            item = {
                "genre_id": genre_id,
                "genre_name": genre_name
            }

            if movie_id:
                item["id"] = movie_id  # optional linkage to movie table

            table.put_item(Item=item)

            return {
                "statusCode": 201,
                "body": json.dumps({
                    "message": "Genre created successfully",
                    "genre_id": genre_id
                }),
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }

        except ClientError as e:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": str(e)})
            }

    return {
        "statusCode": 404,
        "body": json.dumps({"error": "Route not found"})
    }
