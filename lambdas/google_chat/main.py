import os
import boto3
import json
import urllib.request

def lambda_handler(event, context):
    secret_name = os.environ["GOOGLECHAT_SECRET_NAME"]
    sm = boto3.client("secretsmanager")
    webhook = sm.get_secret_value(SecretId=secret_name)["SecretString"]

    payload = { "text": "⚠️ Google Chat alerta recebido com sucesso!" }

    req = urllib.request.Request(
        webhook,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as resp:
            return { "statusCode": resp.status }
    except Exception as e:
        print(f"Erro ao enviar alerta para Google Chat: {e}")
        return { "statusCode": 500 }
