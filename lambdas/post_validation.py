import boto3

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket = event['processed_bucket']
    prefix = f"{event['processed_prefix']}/date={event['run_date']}/"

    response = s3.list_objects_v2(
        Bucket=bucket,
        Prefix=prefix
    )

    if 'Contents' not in response:
        return {
            "status": "FAILED",
            "message": "Processed data missing"
        }

    record_count = len(response['Contents'])

    if record_count == 0:
        return {
            "status": "FAILED",
            "message": "Processed data is empty"
        }

    return {
        "status": "SUCCESS",
        "records": record_count
    }
