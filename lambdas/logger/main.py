import json
import boto3
import os
from datetime import datetime

s3 = boto3.client("s3")
bucket_name = os.environ.get("S3_BUCKET_NAME")

def lambda_handler(event, context):
    """
    Consome mensagens da SQS e salva como arquivos JSON no S3.
    """

    for record in event.get("Records", []):
        try:
            body = json.loads(record["body"])
            timestamp = datetime.utcnow().isoformat()

            s3.put_object(
                Bucket=bucket_name,
                Key=f"logs/{timestamp}.json",
                Body=json.dumps(body),
                ContentType="application/json"
            )

            print(f"[✔] Saved to S3: logs/{timestamp}.json")

        except Exception as e:
            print(f"[✘] Error processing message: {e}")
            raise e

    return {"statusCode": 200}
