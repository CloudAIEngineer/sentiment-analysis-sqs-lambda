## Setting up Athena to Query an S3 Bucket with Exported Files

This guide provides concise steps to configure Amazon Athena to query your S3 bucket containing exported files.

### Prerequisites
1. An S3 bucket with exported files.
2. AWS IAM permissions to create and query Athena tables.
3. Access to the AWS Management Console or AWS CLI.

### Steps

#### 1. Set Permissions for Athena to Access the S3 Bucket
- Attach a bucket policy to your S3 bucket with a principal granting Athena access:
  ```json
  {
      "Version": "2012-10-17",
      "Statement": [
          {
              "Effect": "Allow",
              "Principal": {
                  "Service": "athena.amazonaws.com"
              },
              "Action": [
                  "s3:ListBucket",
                  "s3:GetObject"
              ],
              "Resource": [
                  "arn:aws:s3:::feedback-exports-20250103",
                  "arn:aws:s3:::feedback-exports-20250103/*"
              ]
          }
      ]
  }
  ```
- Replace `your-bucket-name` with the name of your bucket.

#### 2. Configure the Athena Query Results Location
- In the Athena Console, go to **Settings** and set the query results location to an S3 bucket.

#### 3. Create the Athena Table
- Use the following SQL to create a table pointing to your S3 bucket:

  ```sql
  CREATE EXTERNAL TABLE IF NOT EXISTS feedback_table (
    feedbackCategory STRING,
    feedbackId STRING,
    sentiment STRING,
    timestamp STRING,
    month INT
  )
  ROW FORMAT DELIMITED
  FIELDS TERMINATED BY ','
  LINES TERMINATED BY '\n'
  LOCATION 's3://your-bucket-name/'
  TBLPROPERTIES ('skip.header.line.count' = '1');
  ```
- Adjust the `LOCATION` to match your S3 bucket's path.

#### 4. Verify Table and Query
- After creating the table:
  - Run `SELECT * FROM feedback_table LIMIT 10;` in Athena to verify that the data loads correctly.
  - Confirm that the `month` field is properly parsed as an integer if included.