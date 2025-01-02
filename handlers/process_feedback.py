import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
comprehend = boto3.client('comprehend')
DYNAMODB_TABLE = os.environ['DYNAMODB_TABLE']

def handler(event, context):
    table = dynamodb.Table(DYNAMODB_TABLE)

    for record in event['Records']:
        message = json.loads(record['body'])

        try:
            response = comprehend.detect_sentiment(
                Text=message['feedbackText'],
                LanguageCode='en'
            )
            sentiment = response['Sentiment']  
            # Sentiment result (POSITIVE, NEGATIVE, NEUTRAL, MIXED)
        
        except Exception as e:
            sentiment = 'UNKNOWN'
            print(f"Error calling AWS Comprehend: {str(e)}")
        
        table.put_item(
            Item={
                'feedbackId': message['feedbackId'],
                'feedbackText': message['feedbackText'],
                'feedbackCategory': message['feedbackCategory'],
                'timestamp': message['timestamp'],
                'sentiment': sentiment
            }
        )
    
    return {
        'statusCode': 200,
        'body': json.dumps("Processed feedbacks successfully")
    }
