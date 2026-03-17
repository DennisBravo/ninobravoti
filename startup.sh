#!/bin/bash
# Inicia API + Streamlit (stack completo)
pip install -r requirements.txt --quiet
mkdir -p /home/nino_dados /home/nino_dados/memoria_usuarios /home/nino_dados/backups
uvicorn webhook_api:app --host 0.0.0.0 --port 8000 &
python -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true
