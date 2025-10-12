# Sentiment Analysis S3 + Lambda + SQS + DynamoDB

This project implements a **serverless sentiment analysis pipeline** on AWS using **S3**, **SQS**, **Lambda**, **DynamoDB**, and **Comprehend**.  
It processes customer feedback files uploaded to S3, analyzes the sentiment of each feedback message, stores results in DynamoDB, and periodically exports processed data to another S3 bucket.

---

## 📂 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Workflow](#workflow)
3. [Setup](#setup)
4. [Resources](#resources)
5. [Samples](#samples)
6. [License](#license)

---

## 🧩 Architecture Overview

**Components:**

- **S3 (feedback-input)** – stores uploaded `.json` files containing feedback data.
- **Lambda `processFile`** – triggered by S3 upload, reads the file, and sends each feedback entry as a message to **SQS**.
- **SQS (feedbackQueue)** – acts as a buffer for asynchronous processing.
- **Lambda `processFeedback`** – triggered by SQS, performs sentiment analysis using **AWS Comprehend**, and stores results in **DynamoDB**.
- **DynamoDB (FeedbackSentiment)** – stores feedback text, sentiment, timestamp, and exported status.
- **Lambda `exportFeedback`** – runs hourly (via cron), exports unexported items to **S3 (feedback-exports)** as CSV, and marks them as exported.

---

## ⚙️ Workflow

1. **Upload to S3**  
   A `.json` file with an array of feedbacks is uploaded to `feedback-input`.

2. **File Processing (processFile Lambda)**  
   The file is read and each feedback entry is sent to `feedbackQueue` (SQS).

3. **Feedback Analysis (processFeedback Lambda)**  
   Each SQS message triggers sentiment detection via AWS Comprehend.  
   Results are written to DynamoDB with `exported=False`.

4. **Data Export (exportFeedback Lambda)**  
   Once per hour, unexported items are fetched, written to a CSV file, uploaded to `feedback-exports` in S3, and marked as `exported=True` with a 30-day TTL.

---

## 🚀 Setup

### Prerequisites

- **Serverless Framework** installed (`npm install -g serverless`)
- **AWS CLI** configured with appropriate credentials
- Node.js 18+ and Python 3.9+ available locally

### Deploy

```bash
npm install
serverless deploy
```
