import json
import boto3
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, set):
            return list(obj)
        return super().default(obj)

dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table = dynamodb.Table('movies')

def lambda_handler(event, context):
    movie_id = event.get("queryStringParameters", {}).get("id")

    if not movie_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Movie ID is required"})
        }

    response = table.get_item(Key={"id": movie_id})
    movie = response.get("Item")

    if not movie:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Movie not found"})
        }

    return {
        "statusCode": 200,
        "body": json.dumps(movie, cls=DecimalEncoder),
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        }
    }

