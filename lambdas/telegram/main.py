import os
import boto3
import json
import urllib.request

def lambda_handler(event, context):
    # Buscar segredo do webhook
    secret_name = os.environ["TELEGRAM_SECRET_NAME"]
    sm = boto3.client("secretsmanager")
    webhook_url = sm.get_secret_value(SecretId=secret_name)["SecretString"]

    # Criar mensagem
    message = {
        "text": "🚨 Alerta crítico gerado via Lambda!"
    }

    # Enviar POST com urllib
    req = urllib.request.Request(
        webhook_url,
        data=json.dumps(message).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as response:
            status = response.getcode()
            return {"statusCode": status}
    except Exception as e:
        print(f"Erro ao enviar alerta: {e}")
        return {"statusCode": 500}
