import boto3

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket = event['raw_bucket']
    prefix = f"{event['raw_prefix']}/date={event['run_date']}/"

    response = s3.list_objects_v2(
        Bucket=bucket,
        Prefix=prefix
    )

    if 'Contents' not in response:
        return {
            "status": "FAILED",
            "message": "Raw data not found for the given date"
        }

    return {
        "status": "SUCCESS",
        "message": "Raw data is available"
    }
