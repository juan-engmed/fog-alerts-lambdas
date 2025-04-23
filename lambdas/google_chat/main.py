import os
import boto3
import json
import urllib.request

def lambda_handler(event, context):
    # Nome do secret vindo da variável de ambiente
    secret_name = os.environ["GOOGLECHAT_SECRET_NAME"]
    
    # Acessa o Secrets Manager
    sm = boto3.client("secretsmanager")
    secret_raw = sm.get_secret_value(SecretId=secret_name)["SecretString"]
    secret = json.loads(secret_raw)

    # Pega o webhook do Google Chat
    webhook_url = secret["GOOGLECHAT_WEBHOOK"]
    message = {
        "text": "🚨 Alerta recebido via Google Chat!"
    }

    # Envia o POST
    req = urllib.request.Request(
        webhook_url,
        data=json.dumps(message).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as resp:
            return { "statusCode": resp.status }
    except Exception as e:
        print(f"Erro ao enviar alerta para Google Chat: {e}")
        return { "statusCode ": 500 }
