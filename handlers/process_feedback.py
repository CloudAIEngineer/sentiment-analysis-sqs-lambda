import json
import boto3
import os
from datetime import datetime
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")
comprehend = boto3.client("comprehend")
DYNAMODB_TABLE = os.environ["DYNAMODB_TABLE"]

def handler(event, context):
    table = dynamodb.Table(DYNAMODB_TABLE)
    processing_date = datetime.utcnow().strftime("%Y-%m-%d")

    for idx, record in enumerate(event["Records"], start=1):
        message = json.loads(record["body"])
        feedback_id = message.get("feedbackId") or f"id-{int(datetime.utcnow().timestamp()*1000)}"
        feedback_text = message.get("feedbackText", "")

        try:
            sentiment_response = comprehend.detect_sentiment(
                Text=feedback_text,
                LanguageCode="en"
            )
            sentiment = sentiment_response["Sentiment"]
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
                ConditionExpression="attribute_not_exists(feedbackId)"
            )
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "ConditionalCheckFailedException":
                print(f"[SKIP] Duplicate feedbackId={feedback_id}")
            else:
                print(f"[ERROR] DynamoDB error ({error_code}) for {feedback_id}: {e}")
        except Exception as e:
            print(f"[ERROR] Unexpected error for {feedback_id}: {e}")

    return {"statusCode": 200, "body": json.dumps("Batch processed successfully")}
