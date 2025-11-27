import boto3
import csv
import os
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

TABLE_NAME = os.environ['DYNAMODB_TABLE']
EXPORT_BUCKET = os.environ['EXPORT_BUCKET']

def handler(event, context):
    table = dynamodb.Table(TABLE_NAME)
    today = datetime.utcnow().strftime("%Y-%m-%d")

    response = table.query(
        KeyConditionExpression=Key('processingDate').eq(today),
        FilterExpression=Attr('exported').eq("False")
    )

    items = response.get('Items', [])
    if not items:
        print("No new feedbacks to export.")
        return {"statusCode": 200, "body": "No unexported feedbacks."}

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    file_name = f"feedback_export_{timestamp}.csv"
    local_path = f"/tmp/{file_name}"

    with open(local_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["processingDate", "feedbackText", "sentiment", "timestamp", "feedbackId"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for item in items:
            writer.writerow({
                "processingDate": item.get("processingDate", ""),
                "feedbackText": item.get("feedbackText", "").replace("\n", " ").strip(),
                "sentiment": item.get("sentiment", ""),
                "timestamp": item.get("timestamp", ""),
                "feedbackId": item.get("feedbackId", "")
            })

    now = datetime.utcnow()
    key = f"year={now.year}/month={now.month:02d}/day={now.day:02d}/{file_name}"
    s3.upload_file(local_path, EXPORT_BUCKET, key)
    print(f"File uploaded to s3://{EXPORT_BUCKET}/{key}")

    ttl_value = int((datetime.utcnow() + timedelta(days=30)).timestamp())

    for item in items:
        try:
            table.update_item(
                Key={
                    'processingDate': item['processingDate'],
                    'feedbackId': item['feedbackId']
                },
                UpdateExpression="SET exported = :true, exportedAt = :now, #ttl = :ttl",
                ConditionExpression="exported = :false",
                ExpressionAttributeNames={
                    '#ttl': 'ttl'
                },
                ExpressionAttributeValues={
                    ':true': "True",
                    ':false': "False",
                    ':now': datetime.utcnow().isoformat() + "Z",
                    ':ttl': ttl_value
                }
            )
        except Exception as e:
            print(f"[WARN] Failed to update {item['feedbackId']}: {e}")

    print(f"Exported {len(items)} feedbacks successfully.")
    return {"statusCode": 200, "body": f"Exported {len(items)} feedbacks."}
