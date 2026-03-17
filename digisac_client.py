"""
digisac_client.py - Integracao com a API do Digisac
Permite enviar mensagens, buscar conversas e gerenciar tickets.
"""

import os
import requests
from datetime import datetime

try:
    import config
    DIGISAC_TOKEN   = getattr(config, "DIGISAC_TOKEN", "") or getattr(config, "DIGISAC_ACCESS_TOKEN", "")
    DIGISAC_URL     = getattr(config, "DIGISAC_URL", "") or "https://bravoti.digisac.app/api/v1"
    DIGISAC_SERVICE = getattr(config, "DIGISAC_SERVICE_ID", "") or os.environ.get("DIGISAC_SERVICE_ID", "")
except ImportError:
    DIGISAC_TOKEN   = os.environ.get("DIGISAC_TOKEN", "") or os.environ.get("DIGISAC_ACCESS_TOKEN", "")
    DIGISAC_URL     = os.environ.get("DIGISAC_URL", "https://bravoti.digisac.app/api/v1")
    DIGISAC_SERVICE = os.environ.get("DIGISAC_SERVICE_ID", "")


def _headers():
    return {
        "Authorization": "Bearer " + DIGISAC_TOKEN,
        "Content-Type":  "application/json"
    }


def enviar_mensagem(contact_id, ticket_id, texto):
    """
    Envia uma mensagem de texto para um contato via Digisac.
    """
    if not DIGISAC_TOKEN:
        return False, "DIGISAC_TOKEN nao configurado"
    payload = {
        "contactId": contact_id,
        "type":      "text",
        "text":      texto
    }
    if ticket_id:
        payload["ticketId"] = ticket_id
    if DIGISAC_SERVICE:
        payload["serviceId"] = DIGISAC_SERVICE
    try:
        r = requests.post(
            DIGISAC_URL.rstrip("/") + "/messages",
            headers=_headers(),
            json=payload,
            timeout=10
        )
        return r.status_code in (200, 201), r.json() if r.content else {}
    except Exception as e:
        return False, str(e)


def buscar_tickets_abertos(limite=50):
    """
    Busca tickets abertos no Digisac.
    Retorna lista de tickets.
    """
    if not DIGISAC_TOKEN:
        return []
    try:
        r = requests.get(
            DIGISAC_URL.rstrip("/") + "/tickets",
            headers=_headers(),
            params={"status": "open", "limit": limite},
            timeout=10
        )
        if r.status_code == 200:
            dados = r.json()
            return dados.get("data", dados) if isinstance(dados, dict) else dados
        return []
    except Exception:
        return []


def buscar_mensagens_ticket(ticket_id, limite=100):
    """
    Busca todas as mensagens de um ticket especifico.
    Util para aprender com conversas encerradas.
    """
    if not DIGISAC_TOKEN:
        return []
    try:
        r = requests.get(
            DIGISAC_URL.rstrip("/") + "/messages",
            headers=_headers(),
            params={"ticketId": ticket_id, "limit": limite},
            timeout=10
        )
        if r.status_code == 200:
            dados = r.json()
            return dados.get("data", dados) if isinstance(dados, dict) else dados
        return []
    except Exception:
        return []


def buscar_tickets_encerrados(limite=20):
    """
    Busca tickets recentemente encerrados para aprendizado.
    """
    if not DIGISAC_TOKEN:
        return []
    try:
        r = requests.get(
            DIGISAC_URL.rstrip("/") + "/tickets",
            headers=_headers(),
            params={"status": "closed", "limit": limite},
            timeout=10
        )
        if r.status_code == 200:
            dados = r.json()
            return dados.get("data", dados) if isinstance(dados, dict) else dados
        return []
    except Exception:
        return []


def transferir_para_humano(ticket_id, departamento_id=None):
    """
    Transfere um ticket para atendimento humano.
    """
    if not DIGISAC_TOKEN:
        return False, "Token nao configurado"
    payload = {"status": "waiting"}
    if departamento_id:
        payload["departmentId"] = departamento_id
    try:
        r = requests.patch(
            DIGISAC_URL.rstrip("/") + "/tickets/" + ticket_id,
            headers=_headers(),
            json=payload,
            timeout=10
        )
        return r.status_code in (200, 201), r.json() if r.content else {}
    except Exception as e:
        return False, str(e)


def formatar_conversa_para_aprendizado(mensagens):
    """
    Converte lista de mensagens do Digisac em texto formatado
    para ser analisado e aprendido pelo Nino.
    """
    if not mensagens:
        return ""
    linhas = []
    for msg in mensagens:
        remetente = "Cliente" if msg.get("fromMe") == False else "Tecnico"
        texto     = msg.get("text", "") or msg.get("body", "")
        if texto:
            linhas.append(remetente + ": " + texto)
    return "\n".join(linhas)
