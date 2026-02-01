# Self-Healing & Cost-Aware Data Pipeline on AWS

## Overview
This project demonstrates a production-style AWS data engineering pipeline focused on reliability, automation, and cost awareness.

The pipeline is orchestrated using **AWS Step Functions**, validated using **AWS Lambda**, and processes data using **AWS Glue**.  
It is built to **fail fast**, **self-heal through controlled retries**, and **prevent unnecessary processing cost**, simulating real-world data platform behavior.

---

## Architecture

![[Architecture](architecture/architecture.png)](https://github.com/SOURAV416/self-healing-cost-aware-pipeline/blob/2ac32a8d08975a149e00432271e2a1c14e049e31/pipiline_architecture.png)

The architecture separates **control flow** from **data flow**, ensuring better observability and operational control.

---

## High-Level Flow

1. Amazon EventBridge triggers the pipeline on a schedule  
2. AWS Step Functions orchestrates the workflow  
3. Pre-validation Lambda verifies raw data availability  
4. AWS Glue performs batch ETL processing  
5. Post-validation and cost-check Lambdas validate output and cost  
6. Execution state is recorded in DynamoDB  
7. Processed data is queried using Amazon Athena  

---

## Architecture Components

### 1. Amazon EventBridge
EventBridge acts as the **scheduler** for the pipeline.

**Responsibilities:**
- Triggers the pipeline on a nightly schedule
- Acts as the entry point for orchestration
- Eliminates the need for server-based cron jobs

---

### 2. AWS Step Functions
Step Functions is the **central controller** of the pipeline.

**Responsibilities:**
- Controls execution order
- Invokes Lambda and Glue tasks
- Handles retries and failure paths
- Ensures steps execute only after validations succeed

This is the key component that enables **self-healing behavior**.

---

### 3. Pre-Validation Lambda
Executed **before the Glue job**.

**Responsibilities:**
- Checks if raw data exists in Amazon S3
- Validates input folder and file availability
- Fails fast to avoid unnecessary Glue execution and cost

---

### 4. Amazon S3 – Raw
Stores incoming data **as-is**.

**Characteristics:**
- Source of truth
- Immutable storage
- Supports replay and backfills

**Example structure:**
s3://<bucket-name>/raw/date=YYYY-MM-DD/

### 5. AWS Glue – Batch ETL
AWS Glue performs the core data transformation.

**Responsibilities:**
- Reads raw data from S3
- Cleans and transforms data
- Converts data to Parquet format
- Writes partitioned output to processed zone

Glue is executed **synchronously** by Step Functions.

---

### 6. Post-Validation Lambda
Executed **after Glue completes**.

**Responsibilities:**
- Verifies processed data existence
- Performs record count and sanity checks
- Ensures ETL output is usable before marking success

---

### 7. Cost-Check Lambda
Adds **cost-awareness** to the pipeline.

**Responsibilities:**
- Validates Glue runtime against thresholds
- Simulates Athena scan-size checks
- Fails the pipeline if defined cost limits are exceeded

This prevents uncontrolled cloud cost.

---

### 8. Amazon DynamoDB – Execution State Store
DynamoDB stores pipeline execution metadata.

**Stored attributes:**
- Execution date
- Pipeline status
- Retry count
- Timestamps

**Benefits:**
- Controlled retries
- Idempotent execution
- Execution history tracking

---

### 9. Amazon S3 – Processed
Stores transformed, analytics-ready data.

**Characteristics:**
- Parquet format
- Partitioned by date
- Optimized for Athena queries

**Example structure:**
s3://<bucket-name>/processed/date=YYYY-MM-DD/

### 10. Amazon Athena
Athena provides the **query layer** over processed data.

**Use cases:**
- Validate transformed data
- Support analytics and reporting
- Serve data to downstream APIs or frontend applications

---

## Data Flow
S3 Raw → Glue ETL → S3 Processed → Athena

## Control Flow
EventBridge → Step Functions
→ Pre-Validation Lambda
→ Glue ETL
→ Post-Validation Lambda
→ Cost-Check Lambda
→ DynamoDB

## Key Design Decisions

- **Step Functions over Glue triggers:** Enables validation, retries, and orchestration
- **Fail-fast validation:** Avoids unnecessary compute cost
- **Parquet + partitioning:** Improves query performance and reduces Athena scan cost
- **State tracking with DynamoDB:** Prevents duplicate runs and infinite retries
- **Batch processing:** Best suited for periodic, high-volume workloads

---

## Technologies Used
- Amazon EventBridge
- AWS Step Functions
- AWS Lambda
- AWS Glue (PySpark)
- Amazon S3
- Amazon DynamoDB
- Amazon Athena
- Amazon CloudWatch
- AWS IAM
- Python, SQL

---

## Assumptions
- Sample or mock data is used
- Cost checks are threshold-based and simulated
- Security configurations are simplified
- Focus is on backend data engineering, not visualization

---

## Future Enhancements
- Advanced data quality rules
- Notifications using SNS
- Automated backfill workflows
- Dynamic cost thresholds

---

## Author
Sourav Nayek
