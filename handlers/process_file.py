import boto3
import os
import json

s3 = boto3.client('s3')
sqs = boto3.client('sqs')
QUEUE_URL = os.environ['QUEUE_URL']

def handler(event, context):
    record = event['Records'][0]
    bucket_name = record['s3']['bucket']['name']
    object_key = record['s3']['object']['key']

    file_obj = s3.get_object(Bucket=bucket_name, Key=object_key)
    data = file_obj['Body'].read().decode('utf-8')
    feedbacks = json.loads(data)

    if not isinstance(feedbacks, list):
        raise ValueError("Uploaded file must contain an array of feedbacks")

    for feedback in feedbacks:
        sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(feedback)
        )

    print(f"Sent {len(feedbacks)} feedbacks to SQS")
    return {
        "statusCode": 200,
        "body": f"{len(feedbacks)} feedbacks queued successfully"
    }
