"""
persistencia.py - Camada de persistencia segura para o Nino
Garante que dados nao sejam perdidos em deploys do Azure.
"""

import os
import json
import shutil
from datetime import datetime

_BASE = os.path.dirname(os.path.abspath(__file__))
HOME_DIR = os.environ.get("NINO_HOME") or ("/home/nino_dados" if os.name == "posix" else os.path.join(_BASE, "nino_dados"))
MEMORIA_DIR = os.path.join(HOME_DIR, "memoria_usuarios")
CONHECIMENTO_FILE = os.path.join(HOME_DIR, "base_conhecimento_aprendido.json")
APRENDIZADO_FILE = os.path.join(HOME_DIR, "aprendizado.json")
BACKUP_DIR = os.path.join(HOME_DIR, "backups")


def inicializar():
    """Cria estrutura de diretorios na inicializacao."""
    for d in [HOME_DIR, MEMORIA_DIR, BACKUP_DIR]:
        os.makedirs(d, exist_ok=True)
    if not os.path.exists(CONHECIMENTO_FILE):
        _salvar_json(CONHECIMENTO_FILE, {"conhecimentos": []})
    if not os.path.exists(APRENDIZADO_FILE):
        _salvar_json(APRENDIZADO_FILE, [])


def _salvar_json(caminho, dados):
    tmp = caminho + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    os.replace(tmp, caminho)


def _carregar_json(caminho, padrao=None):
    if not os.path.exists(caminho):
        return padrao
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return padrao


def fazer_backup():
    """Faz backup dos arquivos de dados."""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"backup_{timestamp}")
    os.makedirs(backup_path, exist_ok=True)
    for arq in [CONHECIMENTO_FILE, APRENDIZADO_FILE]:
        if os.path.exists(arq):
            shutil.copy2(arq, backup_path)
    if os.path.exists(MEMORIA_DIR):
        shutil.copytree(MEMORIA_DIR, os.path.join(backup_path, "memoria_usuarios"), dirs_exist_ok=True)
    return backup_path
