# Sentiment Analysis S3 + Lambda

This project provides a serverless sentiment analysis pipeline using AWS Lambda, S3, and DynamoDB. It processes customer review data uploaded to an S3 bucket, performs sentiment analysis, and stores the results in DynamoDB.

## Features:
- **Sentiment analysis** for customer reviews.
- **S3 trigger** automatically processes reviews as they are uploaded to the S3 bucket.
- **Lambda functions** handle review extraction, sentiment analysis, and result storage.
- **DynamoDB** stores sentiment analysis results for each review.

## Architecture Overview:
- **ProcessFile**: A Lambda function that extracts feedback data from S3 when a file is uploaded.
- **ProcessFeedback**: A Lambda function that performs sentiment analysis on the extracted feedback.
- **S3 Bucket**: Used to store feedback files that trigger Lambda functions.
- **SQS Queue**: Holds messages for further processing by the AnalyzeSentiment Lambda.

## Workflow:
1. **File Upload to S3**: A file containing customer feedback is uploaded to an S3 bucket. This triggers the `ProcessFile` Lambda.
2. **Feedback processing**: The `ProcessFeedback` Lambda function is triggered by messages in the SQS queue, which contains feedback from the uploaded file. The sentiment analysis results are stored in DynamoDB along with the feedback for further analysis.

## Setup

### Prerequisites:
- **Serverless Framework** installed.
- AWS CLI configured with appropriate credentials.
- S3 bucket created for review uploads (specified in the Serverless configuration, please replace my bucket name).

### Deploy:
1. Clone this repository.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Deploy the service to AWS:
   ```bash
   serverless deploy
   ```

### S3 Bucket:
- The S3 bucket should be configured to trigger the Lambda function (`ProcessFile`) on object creation (i.e., when a new review file is uploaded).

### Lambda Functions:
- **ProcessFile**: This function extracts feedback from the uploaded file and sends it to SQS for further processing.
- **ProcessFeedback**: This function processes feedback from SQS and performs sentiment analysis using AWS Comprehend and stores the sentiment result in DynamoDB.

## Resources:
- **DynamoDB Table**: Stores review data and sentiment analysis results.
- **IAM Roles**: Permissions for Lambda and S3 execution.
- **SQS Queue**: Queue to hold feedback messages for sentiment analysis processing.

## Samples:
In the **reviews** folder, you can find a set of sample files to simulate the upload process. Each file contains up to **10 feedbacks**. You can upload these files to the S3 bucket one by one to test the project.

## License
This project is licensed under the MIT License.