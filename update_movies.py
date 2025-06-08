import json
import boto3

dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table = dynamodb.Table('movies')

def lambda_handler(event, context):
    data = json.loads(event.get("body", "{}"))
    movie_id = data.get("id")

    if not movie_id:
        return {"statusCode": 400, "body": json.dumps({"error": "id is required"})}

    update_expression = "SET "
    expression_values = {}
    for key in data:
        if key != "id":
            update_expression += f"{key} = :{key}, "
            expression_values[f":{key}"] = data[key]
    update_expression = update_expression.rstrip(", ")

    table.update_item(
        Key={"id": movie_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_values
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Movie updated"})
    }
