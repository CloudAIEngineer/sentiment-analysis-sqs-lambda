import boto3
import csv
import os
from datetime import datetime, timedelta

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

TABLE_NAME = os.environ['DYNAMODB_TABLE']
EXPORT_BUCKET = os.environ['EXPORT_BUCKET']

def handler(event, context):
    table = dynamodb.Table(TABLE_NAME)
    today = datetime.utcnow().strftime("%Y-%m-%d")

    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('processingDate').eq(today),
        FilterExpression=boto3.dynamodb.conditions.Attr('exported').eq("False")
    )

    items = response.get('Items', [])
    if not items:
        print("No new feedbacks to export.")
        return {"statusCode": 200, "body": "No unexported feedbacks."}

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    file_name = f"feedback_export_{timestamp}.csv"
    local_path = f"/tmp/{file_name}"

    with open(local_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=items[0].keys())
        writer.writeheader()
        writer.writerows(items)

    now = datetime.utcnow()
    key = f"year={now.year}/month={now.month:02d}/day={now.day:02d}/{file_name}"
    s3.upload_file(local_path, EXPORT_BUCKET, key)
    print(f"File uploaded to s3://{EXPORT_BUCKET}/{key}")

    ttl_value = int((datetime.utcnow() + timedelta(days=30)).timestamp())
    for item in items:
        table.update_item(
            Key={
                'processingDate': item['processingDate'],
                'feedbackId': item['feedbackId']
            },
            UpdateExpression="SET exported=:true, exportedAt=:now, ttl=:ttl",
            ConditionExpression="exported=:false",
            ExpressionAttributeValues={
                ':true': "True",
                ':false': "False",
                ':now': datetime.utcnow().isoformat() + "Z",
                ':ttl': ttl_value
            }
        )

    print(f"Exported {len(items)} feedbacks successfully.")
    return {"statusCode": 200, "body": f"Exported {len(items)} feedbacks."}
