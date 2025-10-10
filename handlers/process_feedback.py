import json
import boto3
import os
from datetime import datetime
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
comprehend = boto3.client('comprehend')
DYNAMODB_TABLE = os.environ['DYNAMODB_TABLE']

def handler(event, context):
    table = dynamodb.Table(DYNAMODB_TABLE)
    processing_date = datetime.utcnow().strftime("%Y-%m-%d")

    for record in event['Records']:
        message = json.loads(record['body'])
        feedback_id = message.get('feedbackId') or f"id-{int(datetime.utcnow().timestamp()*1000)}"
        feedback_text = message.get('feedbackText', '')

        try:
            sentiment_response = comprehend.detect_sentiment(
                Text=feedback_text,
                LanguageCode='en'
            )
            sentiment = sentiment_response['Sentiment']
        except Exception as e:
            print(f"Comprehend error: {e}")
            sentiment = "UNKNOWN"

        try:
            table.put_item(
                Item={
                    "processingDate": processing_date,
                    "feedbackId": feedback_id,
                    "feedbackText": feedback_text,
                    "sentiment": sentiment,
                    "exported": "False",
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                },
                ConditionExpression="attribute_not_exists(feedbackId)"  # защита от дубликатов
            )
        except ClientError as e:
            if
