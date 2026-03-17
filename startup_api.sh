#!/bin/bash
# Inicia SOMENTE a API Webhook (deploy Azure nino-bravoti-api)
pip install -r requirements_api.txt --quiet
mkdir -p /home/nino_dados /home/nino_dados/memoria_usuarios /home/nino_dados/backups
uvicorn webhook_api:app --host 0.0.0.0 --port 8000
