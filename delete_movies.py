import json
import boto3

dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table = dynamodb.Table('movies')

def lambda_handler(event, context):
    data = json.loads(event.get("body", "{}"))
    movie_id = data.get("id")

    if not movie_id:
        return {"statusCode": 400, "body": json.dumps({"error": "id is required"})}

    table.delete_item(Key={"id": movie_id})

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Movie deleted"})
    }


