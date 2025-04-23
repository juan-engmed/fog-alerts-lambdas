import os
import boto3
import json
import urllib.request

def lambda_handler(event, context):
    # Nome do secret vindo da variável de ambiente
    secret_name = os.environ["TELEGRAM_SECRET_NAME"]
    
    # Acessa o Secrets Manager
    sm = boto3.client("secretsmanager")
    secret_raw = sm.get_secret_value(SecretId=secret_name)["SecretString"]
    secret = json.loads(secret_raw)

    # Extrai os dados do Telegram
    token = secret["TELEGRAM_TOKEN"]
    chat_id = secret["TELEGRAM_CHAT_ID"]
    message = "🚨 Alerta recebido!"

    # Monta a URL do Telegram
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }

    # Envia o POST
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as response:
            status = response.getcode()
            return {"statusCode": status}
    except Exception as e:
        print(f"Erro ao enviar alerta: {e}")
        return {"statusCode ": 500}
