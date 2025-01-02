import boto3
import os
import json

s3 = boto3.client('s3')
sqs = boto3.client('sqs')
QUEUE_URL = os.environ['QUEUE_URL']

def handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']

    file_obj = s3.get_object(Bucket=bucket_name, Key=object_key)
    feedbacks = json.loads(file_obj['Body'].read().decode('utf-8'))

    if not isinstance(feedbacks, list):
        raise ValueError("Uploaded file must contain an array of feedbacks")

    for feedback in feedbacks:
        sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(feedback)
        )

    return {
        "statusCode": 200,
        "body": f"{len(feedbacks)} feedbacks added to SQS successfully"
    }

