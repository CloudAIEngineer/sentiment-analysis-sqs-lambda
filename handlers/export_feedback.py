import boto3
import csv
import os
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

TABLE_NAME = os.environ['DYNAMODB_TABLE']
INDEX_NAME = os.environ['DYNAMODB_INDEX']
BUCKET_NAME = os.environ['BUCKET_NAME']

def handler(event, context):
    table = dynamodb.Table(TABLE_NAME)
    
    response = table.query(
        IndexName=INDEX_NAME,
        KeyConditionExpression=boto3.dynamodb.conditions.Key('exported').eq('False')
    )
    
    items = response['Items']
    if not items:
        print("No new feedbacks to export.")
        return
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_name = f'feedback_export_{timestamp}.csv'
    with open(f'/tmp/{file_name}', mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=items[0].keys())
        writer.writeheader()
        writer.writerows(items)
    
    s3.upload_file(f'/tmp/{file_name}', BUCKET_NAME, file_name)
    print(f'File {file_name} uploaded to S3 bucket {BUCKET_NAME}')
    
    for item in items:
        table.update_item(
            Key={'feedbackId': item['feedbackId']},
            UpdateExpression='SET exported = :true',
            ExpressionAttributeValues={':true': "True"}
        )

    print("Exported feedbacks marked as exported.")
