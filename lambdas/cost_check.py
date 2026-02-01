def lambda_handler(event, context):
    glue_runtime_minutes = event.get('glue_runtime_minutes', 0)
    athena_scan_gb = event.get('athena_scan_gb', 0)

    MAX_RUNTIME = 30      # minutes
    MAX_SCAN_GB = 5       # GB

    if glue_runtime_minutes > MAX_RUNTIME:
        return {
            "status": "FAILED",
            "message": "Glue runtime exceeded threshold"
        }

    if athena_scan_gb > MAX_SCAN_GB:
        return {
            "status": "FAILED",
            "message": "Athena scan size exceeded threshold"
        }

    return {
        "status": "SUCCESS",
        "message": "Cost checks passed"
    }
