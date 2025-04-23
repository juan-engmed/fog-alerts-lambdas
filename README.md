# fog-alerts-lambdas

Este repositório contém o código das funções AWS Lambda do projeto Fog Alerts:

- `logger`: registra mensagens no S3
- `telegram`: envia alertas críticos para o Telegram
- `google_chat`: envia alertas para um espaço do Google Chat

Cada Lambda possui seu workflow de CI/CD independente via GitHub Actions.
