"""
milvus_client.py - Integracao com o Milvus HelpDesk
Permite criar chamados, buscar tickets e notificar tecnicos.
"""

import os
import requests

try:
    import config
    MILVUS_TOKEN     = getattr(config, "MILVUS_TOKEN", "") or os.environ.get("MILVUS_TOKEN", "")
    MILVUS_URL       = "https://app.milvus.com.br/api/v1"
    MILVUS_CLIENTE = getattr(config, "CLIENTE_ID", "") or os.environ.get("CLIENTE_ID", "")
    MILVUS_CATEGORIA = getattr(config, "CATEGORIA_ID", "") or os.environ.get("CATEGORIA_ID", "")
except ImportError:
    MILVUS_TOKEN     = os.environ.get("MILVUS_TOKEN", "")
    MILVUS_URL       = "https://app.milvus.com.br/api/v1"
    MILVUS_CLIENTE   = os.environ.get("CLIENTE_ID", "")
    MILVUS_CATEGORIA = os.environ.get("CATEGORIA_ID", "")


def _headers():
    return {
        "Authorization": "Bearer " + MILVUS_TOKEN,
        "Content-Type":  "application/json"
    }


def criar_chamado(nome, email, descricao, urgencia="medium", historico=""):
    """
    Cria um novo chamado no Milvus HelpDesk.

    urgencia: low | medium | high
    Retorna (sucesso, dados_resposta)
    """
    if not MILVUS_TOKEN:
        return False, {"error": "MILVUS_TOKEN nao configurado"}
    try:
        r = requests.post(
            MILVUS_URL + "/issue",
            headers=_headers(),
            json={
                "clientId":       MILVUS_CLIENTE,
                "categoryId":     MILVUS_CATEGORIA,
                "title":          "[Nino] " + descricao[:80],
                "description":    historico or descricao,
                "priority":       urgencia,
                "requesterName":  nome,
                "requesterEmail": email,
            },
            timeout=10
        )
        return r.status_code in (200, 201), r.json() if r.content else {}
    except Exception as e:
        return False, {"error": str(e)}


def abrir_chamado(nome, email, descricao, historico_texto, urgencia="medium"):
    """
    Alias para criar_chamado - usado pelo webhook do Digisac.
    historico_texto: string com o historico formatado da conversa.
    """
    return criar_chamado(nome, email, descricao, urgencia=urgencia, historico=historico_texto)


def buscar_chamados_novos(limite=20):
    """
    Busca chamados novos criados diretamente no Milvus.
    Usado na Etapa 3 — chamados criados diretamente.
    """
    if not MILVUS_TOKEN:
        return []
    try:
        r = requests.get(
            MILVUS_URL + "/issues",
            headers=_headers(),
            params={"status": "new", "limit": limite},
            timeout=10
        )
        if r.status_code == 200:
            dados = r.json()
            return dados.get("data", dados) if isinstance(dados, dict) else dados
        return []
    except Exception:
        return []


def buscar_chamado(chamado_id):
    """Busca detalhes de um chamado especifico."""
    if not MILVUS_TOKEN:
        return None
    try:
        r = requests.get(
            MILVUS_URL + "/issues/" + str(chamado_id),
            headers=_headers(),
            timeout=10
        )
        if r.status_code == 200:
            return r.json()
        return None
    except Exception:
        return None


def atualizar_chamado(chamado_id, status=None, observacao=None):
    """Atualiza status ou adiciona observacao em um chamado."""
    if not MILVUS_TOKEN:
        return False, "Token nao configurado"
    payload = {}
    if status:
        payload["status"] = status
    if observacao:
        payload["observation"] = observacao
    try:
        r = requests.patch(
            MILVUS_URL + "/issues/" + str(chamado_id),
            headers=_headers(),
            json=payload,
            timeout=10
        )
        return r.status_code in (200, 201), r.json() if r.content else {}
    except Exception as e:
        return False, str(e)


def formatar_chamado_para_digisac(chamado):
    """
    Converte dados de um chamado Milvus em mensagem
    formatada para enviar ao cliente via Digisac.
    """
    if not chamado:
        return ""
    titulo  = chamado.get("title", "Sem titulo")
    status  = chamado.get("status", "novo")
    criado  = chamado.get("created_at", "")[:10] if chamado.get("created_at") else ""
    return (
        "Ola! Identificamos seu chamado no sistema.\n\n"
        "Titulo: " + titulo + "\n"
        "Status: " + status + "\n"
        "Data: " + criado + "\n\n"
        "Nossa equipe tecnica entrar em contato em breve. "
        "Se precisar de suporte imediato, responda aqui!"
    )
