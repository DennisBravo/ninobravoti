"""
webhook_api.py - API FastAPI para receber webhooks do Digisac
"""

import os
import json
import re
import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from typing import Dict, Any, List, Tuple, Optional

from nino_core import gerar_resposta, classificar_problema, carregar_historico_usuario
from digisac_client import enviar_mensagem, transferir_para_humano
from milvus_client import abrir_chamado as abrir_chamado_milvus
from prompt_fluxo_atendimento import FLUXO_ATENDIMENTO_PROMPT

try:
    from persistencia import inicializar
    inicializar()
except ImportError:
    os.makedirs("memoria_usuarios", exist_ok=True)

app = FastAPI(title="Nino Webhook API")

# Cooldown 15 segundos - evita loop sem bloquear conversa
COOLDOWN_SEGUNDOS = 15
_ultima_resposta_por_contato: Dict[str, float] = {}

# Historico de conversa por contato - mantem contexto
CONVERSAS_DIR = "conversas_ativas"
MAX_MENSAGENS_CONVERSA = 10  # ultimas 10 trocas user/assistant (menos = resposta mais rapida)


def _caminho_conversa(contact_id: str) -> str:
    nome = str(contact_id).replace("/", "_").replace("\\", "_")[:80]
    return os.path.join(CONVERSAS_DIR, f"{nome}.json")


def _carregar_conversa(contact_id: str) -> Tuple[List[Dict[str, str]], Dict[str, Any]]:
    """Retorna (mensagens, metadata)."""
    os.makedirs(CONVERSAS_DIR, exist_ok=True)
    caminho = _caminho_conversa(contact_id)
    meta = {"aguardando_dados_chamado": False, "categoria": "outros"}
    if os.path.exists(caminho):
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                dados = json.load(f)
                msgs = dados.get("mensagens", [])[-MAX_MENSAGENS_CONVERSA:]
                meta.update(dados.get("meta", {}))
                return msgs, meta
        except Exception:
            pass
    return [], meta


def _salvar_conversa(contact_id: str, mensagens: List[Dict[str, str]], meta: Optional[Dict[str, Any]] = None):
    os.makedirs(CONVERSAS_DIR, exist_ok=True)
    caminho = _caminho_conversa(contact_id)
    payload = {"mensagens": mensagens[-MAX_MENSAGENS_CONVERSA:], "meta": meta or {}}
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def _formatar_historico_para_chamado(mensagens: List[Dict[str, str]]) -> str:
    """Formata o historico da conversa para o corpo do chamado Milvus."""
    linhas = [
        "CHAMADO GERADO VIA NINO - BRAVO TI (WhatsApp)",
        "",
        "HISTORICO DO ATENDIMENTO",
        "─────────────────────────",
    ]
    for i, msg in enumerate(mensagens, 1):
        role = "Nino" if msg["role"] == "assistant" else "Usuario"
        conteudo = (msg.get("content") or "").replace("**", "").replace("*", "").replace("`", "")
        linhas.append(f"[{i}] {role}:")
        linhas.append(conteudo)
        linhas.append("")
    return "\n".join(linhas)


def _extrair_nome_email(texto: str) -> Optional[Tuple[str, str]]:
    """Tenta extrair nome e email da mensagem do usuario. Retorna (nome, email) ou None."""
    email_re = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
    match = email_re.search(texto)
    if not match:
        return None
    email = match.group(0)
    resto = texto[:match.start()].strip() + " " + texto[match.end():].strip()
    nome = resto.strip() or "Cliente WhatsApp"
    if len(nome) < 2:
        nome = "Cliente WhatsApp"
    return (nome.strip(), email)


def _nino_pediu_dados_chamado(resposta: str) -> bool:
    """Verifica se a resposta do Nino pediu nome e email para abrir chamado."""
    r = resposta.lower()
    return ("nome" in r and "email" in r) or "me informe" in r or "informe seu" in r


@app.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok"}


def _gerar_resposta_simples(mensagens: List[Dict[str, str]], prompt_usuario: str, historico_anterior=None) -> str:
    """
    Usa gerar_resposta com fluxo de atendimento (max 3 perguntas, escalar para humano).
    """
    try:
        return gerar_resposta(
            mensagens=mensagens,
            prompt_usuario=prompt_usuario,
            historico_anterior=historico_anterior,
            contexto_sharepoint="",
            contexto_fluxo=FLUXO_ATENDIMENTO_PROMPT,
        )
    except Exception as e:
        return f"Desculpe, tive um problema tecnico ao responder. (erro: {e})"


def _extrair_dados_digisac(data: dict) -> dict | None:
    """
    Extrai contact_id, ticket_id e texto do payload do Digisac.
    Suporta formato plano e formato aninhado (data.message, data.contact, etc).
    """
    inner = data.get("data") or data

    contact_id = None
    ticket_id = None
    texto = None
    direction = None
    from_me = False

    if isinstance(inner, dict):
        msg = inner.get("message") or inner
        if isinstance(msg, dict):
            texto = msg.get("text") or msg.get("content") or msg.get("body")
            direction = msg.get("direction") or msg.get("directionType")
            from_me = msg.get("fromMe", False) or msg.get("from_me", False)

        contact = inner.get("contact") or {}
        if isinstance(contact, dict):
            contact_id = contact.get("id") or contact.get("contactId")
        elif isinstance(contact, str):
            contact_id = contact

        ticket = inner.get("ticket") or {}
        if isinstance(ticket, dict):
            ticket_id = ticket.get("id") or ticket.get("ticketId")
        elif isinstance(ticket, str):
            ticket_id = ticket

    if not contact_id:
        contact_id = data.get("contactId") or (inner.get("contactId") if isinstance(inner, dict) else None)
    if not ticket_id:
        ticket_id = data.get("ticketId") or (inner.get("ticketId") if isinstance(inner, dict) else None)
    if not texto:
        texto = data.get("text") or data.get("body") or data.get("message")
        if not texto and isinstance(inner, dict):
            texto = inner.get("text") or inner.get("body")

    if direction in ("out", "outgoing", "sent") or from_me:
        return None

    if contact_id and texto:
        return {
            "contact_id": str(contact_id),
            "ticket_id": ticket_id,
            "texto": str(texto).strip(),
        }
    return None


@app.post("/webhook/test")
async def webhook_test(body: Dict[str, Any]) -> JSONResponse:
    """
    Endpoint simples para teste manual (curl / Postman).
    Espera:
    {
      "message": "oi nino",
      "phone":   "5511999999999"
    }
    """
    texto = body.get("message") or body.get("text") or ""
    telefone = body.get("phone") or body.get("number") or ""

    if not texto:
        return JSONResponse({"error": "message/text vazio"}, status_code=400)

    mensagens = [{"role": "user", "content": texto}]
    resposta = _gerar_resposta_simples(mensagens, texto)

    return JSONResponse({"resposta": resposta, "telefone": telefone})


@app.post("/webhook/digisac")
async def webhook_digisac(request: Request) -> JSONResponse:
    """
    Webhook chamado pelo Digisac ao receber mensagem no WhatsApp.
    """
    try:
        data = await request.json()
    except Exception:
        data = {}

    dados = _extrair_dados_digisac(data)

    if not dados:
        return JSONResponse(
            {"status": "ignored", "reason": "payload sem texto/contactId ou mensagem enviada pelo bot"},
            status_code=200,
        )

    contact_id = dados["contact_id"]

    # COOLDOWN: evita loop - nao responde de novo antes de 15 segundos
    agora = time.time()
    ultima = _ultima_resposta_por_contato.get(contact_id, 0)
    if agora - ultima < COOLDOWN_SEGUNDOS:
        return JSONResponse(
            {"status": "ignored", "reason": "cooldown", "segundos_restantes": int(COOLDOWN_SEGUNDOS - (agora - ultima))},
            status_code=200,
        )
    ticket_id = dados.get("ticket_id")
    texto = dados["texto"]

    if not texto:
        return JSONResponse({"status": "ok"}, status_code=200)

    # Carrega historico da CONVERSA (contexto) e metadata
    mensagens, meta = _carregar_conversa(contact_id)

    # Se estava aguardando dados para chamado e usuario enviou nome+email
    if meta.get("aguardando_dados_chamado"):
        parsed = _extrair_nome_email(texto)
        if parsed:
            nome, email = parsed
            descricao = meta.get("descricao_chamado", "Suporte via WhatsApp")
            historico_txt = _formatar_historico_para_chamado(mensagens)
            ok_chamado, resp_milvus = abrir_chamado_milvus(
                nome=nome, email=email, descricao=descricao,
                historico_texto=historico_txt, urgencia="medium"
            )
            meta["aguardando_dados_chamado"] = False
            if ok_chamado and ticket_id:
                transferir_para_humano(ticket_id)
            resposta = (
                "Chamado registrado! Um analista da Bravo TI entrara em contato em breve. "
                "Obrigado pela paciencia!"
            )
            mensagens.append({"role": "user", "content": texto})
            mensagens.append({"role": "assistant", "content": resposta})
            _salvar_conversa(contact_id, mensagens, meta)
            ok, detalhe = enviar_mensagem(contact_id=contact_id, ticket_id=ticket_id, texto=resposta)
            _ultima_resposta_por_contato[contact_id] = time.time()
            return JSONResponse({
                "status": "ok" if ok else "erro_envio",
                "chamado_aberto": ok_chamado,
                "contactId": contact_id,
                "ticketId": ticket_id,
                "resposta": resposta,
            })
        # Usuario nao enviou nome/email no formato esperado - deixa o Nino responder

    mensagens.append({"role": "user", "content": texto})

    historico = carregar_historico_usuario(contact_id)
    historico_atendimentos = historico.get("atendimentos", [])[-3:]
    historico_anterior = [
        {"data": a.get("data"), "problema_relatado": a.get("problema_relatado"), "status": a.get("status")}
        for a in historico_atendimentos
    ]

    categoria = classificar_problema(texto)
    meta["categoria"] = categoria
    resposta = _gerar_resposta_simples(mensagens, texto, historico_anterior)

    # Se o Nino pediu nome/email para abrir chamado, marca para proxima mensagem
    if _nino_pediu_dados_chamado(resposta):
        meta["aguardando_dados_chamado"] = True
        first_user_msg = next((m.get("content", "") for m in mensagens if m.get("role") == "user"), texto)
        meta["descricao_chamado"] = (first_user_msg or texto)[:80] or "Suporte via WhatsApp"

    # Salva conversa com a resposta do Nino para manter contexto
    mensagens.append({"role": "assistant", "content": resposta})
    _salvar_conversa(contact_id, mensagens, meta)

    ok, detalhe = enviar_mensagem(
        contact_id=contact_id,
        ticket_id=ticket_id,
        texto=resposta,
    )

    # Registra cooldown apos enviar (evita loop)
    _ultima_resposta_por_contato[contact_id] = time.time()

    return JSONResponse(
        {
            "status": "ok" if ok else "erro_envio",
            "categoria": categoria,
            "contactId": contact_id,
            "ticketId": ticket_id,
            "resposta": resposta,
            "detalhe_envio": detalhe,
        }
    )
