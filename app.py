import streamlit as st
import requests
import urllib.parse
import io
import base64
import random
from PIL import Image as _PIL_Image
import config
from nino_core import (
    gerar_resposta_stream,
    classificar_problema,
    carregar_historico_usuario,
    salvar_atendimento,
    atualizar_avaliacao,
    tem_historico_recente,
)

# AVATARES
ROBOT_AVATAR = "data:image/png;base64,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as70h4rs/wANRGtuQcuUWlrZHLKWUyUI+67132+8D8RWxF1tDram3UJWhQ2UlQ3BHqKinUPh40ozUrfnY01bpqv/AFdsV7O5v5kJ9xR/rJNA0v4hNMM/caiQL4m23Nwe7BuOzLij5JJPKo+gJPpUrghQBBBB7iKprlnBGeZbuJ5sE+KGbjG/60f/AM15mPaecWemEkDHLgLvBb6dgmeiTHUPINvbKHxSAfWgu9Sq54trLrRAKGM50Pu74HRcm0dT8Q2okH+0KmXE81gZClARar/bXld7NxtbrBSfIqIKfwUaDJ6UpQKUpQKV+E7DesIzLUeLj/M1ExbLL9K/VZt1qcUCfVxfKgD5n4UGcVxSZDEVhb8l5thpA3UtxQSlI8yT3VWvJtVOIy9KXHw3Rx2zIV0RIuKw4seuxKUg/Hf51Glx0H4k9TZhkZ5kzENhZ3LUy4cyEj7jLAKB8OlBNGqfFXpriCZESzSVZRdG90pagqHYBX3nj7u3qnmqn+ruv2o2pwXbps76vtLiultt4KEL8gs/aX8CdvSrD4lwTY7GUhzKMvuFw22KmoTKWEn05lcxqfNP9I9OcEaQMaxWBGfT/wCqdT2z5Pn2i91fIECgojpPwxalZyI82XB/k5aXdle1XBBS4pPmhroo+m/KD51c7RjQHAdMC3Nt8JVzvQRyquU0BTg8+zT3N7+nXbpualmlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlApSlB//Z"
USER_AVATAR = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMDAgMTAwIiB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCI+CiAgPCEtLSBGdW5kbyBjaXJjdWxhciB2ZXJtZWxobyAtLT4KICA8Y2lyY2xlIGN4PSI1MCIgY3k9IjUwIiByPSI1MCIgZmlsbD0iI0NDMDAwMCIvPgogIDwhLS0gQ2FiZcOnYSAoY8OtcmN1bG8gYnJhbmNvKSAtLT4KICA8Y2lyY2xlIGN4PSI1MCIgY3k9IjM1IiByPSIxNiIgZmlsbD0id2hpdGUiLz4KICA8IS0tIENvcnBvIChhcmNvIGJyYW5jbykgLS0+CiAgPHBhdGggZD0iTTE4IDg1IFExOCA2MiA1MCA2MiBRODIgNjIgODIgODUiIGZpbGw9IndoaXRlIi8+Cjwvc3ZnPgo="

# PAGE CONFIG
_icon_bytes = base64.b64decode(ROBOT_AVATAR.split(",", 1)[1])
_icon_img = _PIL_Image.open(io.BytesIO(_icon_bytes))

st.set_page_config(
    page_title="nino v.1 | Bravo TI",
    page_icon=_icon_img,
    layout="centered",
)

st.markdown("""
<style>
  .nino-header { display:flex; align-items:center; gap:12px; margin-bottom:4px; }
  .nino-title  { font-size:2.8rem; font-weight:900; letter-spacing:-1px; margin:0; }
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="nino-header">
  <img src="{ROBOT_AVATAR}" width="52" style="border-radius:10px;"/>
  <span class="nino-title">nino v.1</span>
</div>
""", unsafe_allow_html=True)
st.caption("Seu suporte tecnico inteligente · Bravo TI")
st.divider()

FRASES_ABERTURA = [
    "Ola! Sou o Nino, suporte tecnico da **Bravo TI**. Como posso te ajudar hoje?",
    "Oi! Aqui e o Nino da **Bravo TI**. Qual e o problema tecnico?",
    "Ola! To aqui pra resolver seus pepinos de TI! O que esta acontecendo?",
    "Oi! Sou o Nino, assistente tecnico da **Bravo TI**. Me conta o que ta rolando!",
]

FRASES_DESPEDIDA = [
    "Fico feliz que resolveu! Qualquer coisa e so chamar.",
    "Otimo! Missao cumprida! Ate a proxima.",
    "Que bom! Sempre que precisar estou aqui.",
    "Perfeito! Problema resolvido e sempre uma boa noticia!",
]

FRASES_ESCALADA = [
    "Vou chamar reforchos! Nossa equipe tecnica vai te atender em breve.",
    "Esse caso precisa de um olhar mais especializado. Abrindo chamado agora!",
    "Sem problema, nosso time de especialistas vai resolver isso pra voce!",
]


def _init_state():
    defaults = {
        "messages":          [],
        "aguardando_acao":   False,
        "abrir_chamado":     False,
        "resolvido":         False,
        "avaliado":          False,
        "avaliacao_nota":    0,
        "frase_despedida":   random.choice(FRASES_DESPEDIDA),
        "frase_escalada":    random.choice(FRASES_ESCALADA),
        "usuario_id":        "",
        "categoria_atual":   "outros",
        "primeiro_problema": "",
        "historico_usuario": [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


_init_state()

# ─── IDENTIFICACAO DO USUARIO ───────────────────────────────
if not st.session_state.usuario_id:
    st.markdown("#### Ola! Como devo te chamar?")
    col_nome, col_email = st.columns(2)
    with col_nome:
        nome_input = st.text_input("Seu nome", placeholder="Ex: Joao Silva", key="input_nome")
    with col_email:
        email_input = st.text_input("Seu e-mail (opcional)", placeholder="joao@empresa.com", key="input_email")

    if st.button("Pronto, pode comecar!", type="primary"):
        if nome_input.strip():
            uid = email_input.strip() if email_input.strip() else nome_input.strip()
            st.session_state.usuario_id = uid
            dados = carregar_historico_usuario(uid)
            st.session_state.historico_usuario = dados.get("atendimentos", [])
            recentes = tem_historico_recente(uid, horas=48)
            if recentes:
                ultimo = recentes[-1]
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": (
                        f"Ola, **{nome_input.split()[0]}**! Vi que voce esteve aqui recentemente "
                        f"com um problema de *{ultimo.get('problema_relatado','TI')}*. "
                        f"Esta relacionado ao mesmo problema ou e algo novo?"
                    )
                })
            else:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Ola, **{nome_input.split()[0]}**! " + random.choice(FRASES_ABERTURA)
                })
            st.rerun()
    st.stop()


# ─── HELPERS ────────────────────────────────────────────────
def formatar_historico_chamado(nome, email, urgencia):
    linhas = [
        "╔══════════════════════════════════════╗",
        "   CHAMADO GERADO VIA NINO v.1 - BRAVO TI",
        "╚══════════════════════════════════════╝",
        "",
        "DADOS DO SOLICITANTE",
        "─────────────────────",
        f"Nome.....: {nome}",
        f"E-mail...: {email}",
        f"Urgencia.: {urgencia}",
        f"Categoria: {st.session_state.categoria_atual.upper()}",
        "",
        "HISTORICO DO ATENDIMENTO",
        "─────────────────────────",
    ]
    for i, msg in enumerate(st.session_state.messages, 1):
        role = "Nino (Tecnico)" if msg["role"] == "assistant" else "Usuario"
        conteudo = msg["content"].replace("**","").replace("*","").replace("`","")
        linhas.append(f"[{i}] {role}:")
        linhas.append(conteudo)
        linhas.append("")
    return "\n".join(linhas)


def abrir_chamado_milvus(nome, email, urgencia, descricao):
    historico = formatar_historico_chamado(nome, email, urgencia)
    url     = "https://app.milvus.com.br/api/v1/issue"
    token   = getattr(config, "MILVUS_TOKEN", "")
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {
        "clientId":       getattr(config, "CLIENTE_ID", ""),
        "categoryId":     getattr(config, "CATEGORIA_ID", ""),
        "title":          f"[Nino] {descricao[:80]}",
        "description":    historico,
        "priority":       urgencia,
        "requesterName":  nome,
        "requesterEmail": email,
    }
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=10)
        return r.status_code in (200, 201), r.json() if r.content else {}
    except Exception as e:
        return False, {"error": str(e)}


# ─── RENDERIZAR HISTORICO ────────────────────────────────────
for msg in st.session_state.messages:
    avatar = ROBOT_AVATAR if msg["role"] == "assistant" else USER_AVATAR
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])


# ─── AVALIACAO POR ESTRELAS ──────────────────────────────────
if st.session_state.resolvido and not st.session_state.avaliado:
    with st.chat_message("assistant", avatar=ROBOT_AVATAR):
        st.markdown("Como voce avalia este atendimento?")
        cols = st.columns(5)
        for i, col in enumerate(cols, 1):
            with col:
                if st.button("⭐" * i, key=f"star_{i}"):
                    st.session_state.avaliacao_nota = i
                    st.session_state.avaliado = True
                    atualizar_avaliacao(st.session_state.usuario_id, i)
                    msg_aval = f"Obrigado pela avaliacao de **{i} estrela(s)**! " + st.session_state.frase_despedida
                    st.session_state.messages.append({"role": "assistant", "content": msg_aval})
                    st.balloons()
                    st.rerun()
    st.stop()

if st.session_state.resolvido and st.session_state.avaliado:
    st.success(f"Atendimento encerrado · Avaliacao: {'⭐' * st.session_state.avaliacao_nota}")
    if st.button("Novo atendimento"):
        uid = st.session_state.usuario_id
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.session_state.usuario_id = uid
        st.rerun()
    st.stop()


# ─── ABERTURA DE CHAMADO ─────────────────────────────────────
if st.session_state.abrir_chamado:
    with st.chat_message("assistant", avatar=ROBOT_AVATAR):
        st.markdown("### Chamado Tecnico")
        st.info("Vou registrar seu chamado e direcionar voce para um especialista **Bravo TI**.")
        with st.form("form_chamado"):
            col1, col2 = st.columns(2)
            with col1:
                nome_form = st.text_input("Nome completo *")
            with col2:
                email_form = st.text_input("E-mail *")
            urgencia_form = st.selectbox("Urgencia", [
                "Baixa - posso aguardar",
                "Media - preciso hoje",
                "Alta - parado sem produzir"
            ])
            descricao_form = st.text_area("Descreva o problema", value=st.session_state.primeiro_problema[:200])
            enviar = st.form_submit_button("Abrir Chamado", type="primary")

        if enviar:
            if not nome_form or not email_form:
                st.warning("Nome e e-mail sao obrigatorios.")
            else:
                urg_map = {"Baixa - posso aguardar": "low", "Media - preciso hoje": "medium", "Alta - parado sem produzir": "high"}
                sucesso, _ = abrir_chamado_milvus(nome_form, email_form, urg_map.get(urgencia_form, "medium"), descricao_form)
                if sucesso:
                    st.success("Chamado registrado com sucesso!")
                else:
                    st.warning("Nao foi possivel registrar automaticamente. Use o WhatsApp abaixo.")
                salvar_atendimento(
                    identificador=st.session_state.usuario_id,
                    conversa=st.session_state.messages,
                    categoria=st.session_state.categoria_atual,
                    problema_relatado=st.session_state.primeiro_problema[:200],
                    status="escalado"
                )
                wpp   = getattr(config, "WHATSAPP_SUPORTE", "5511999999999")
                texto = urllib.parse.quote(f"Ola! Sou {nome_form}. Problema: {descricao_form[:150]}")
                st.markdown(f"[Abrir no WhatsApp](https://wa.me/{wpp}?text={texto})")
                st.session_state.messages.append({"role": "assistant", "content": st.session_state.frase_escalada})
                st.session_state.abrir_chamado = False
                st.session_state.resolvido     = True
                st.rerun()
    st.stop()


# ─── BOTOES POS-RESPOSTA ─────────────────────────────────────
if st.session_state.aguardando_acao:
    with st.chat_message("assistant", avatar=ROBOT_AVATAR):
        st.markdown("Conseguimos resolver? Posso continuar te ajudando aqui ou, se preferir, te transfiro para um dos nossos analistas. 😊")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("✅ Resolveu!", key="btn_resolveu"):
                st.session_state.aguardando_acao = False
                st.session_state.resolvido = True
                salvar_atendimento(
                    identificador=st.session_state.usuario_id,
                    conversa=st.session_state.messages,
                    categoria=st.session_state.categoria_atual,
                    problema_relatado=st.session_state.primeiro_problema[:200],
                    status="resolvido"
                )
                st.rerun()
        with col2:
            if st.button("🔄 Continuar tentando", key="btn_continuar"):
                st.session_state.aguardando_acao = False
                st.rerun()
        with col3:
            if st.button("👨‍🔧 Falar com analista", key="btn_analista"):
                st.session_state.aguardando_acao = False
                st.session_state.abrir_chamado   = True
                st.rerun()
    st.stop()


# ─── INPUT DO USUARIO ────────────────────────────────────────
prompt = st.chat_input("Digite sua duvida de TI aqui...")

if prompt:
    categoria = classificar_problema(prompt)
    if categoria != "outros":
        st.session_state.categoria_atual = categoria

    if not st.session_state.primeiro_problema:
        st.session_state.primeiro_problema = prompt

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=ROBOT_AVATAR):
        container = st.empty()
        full_response = ""
        try:
            stream = gerar_resposta_stream(
                mensagens=st.session_state.messages,
                prompt_usuario=prompt,
                historico_anterior=st.session_state.historico_usuario
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                full_response += delta
                container.markdown(full_response + "▌")
            container.markdown(full_response)
        except Exception as e:
            full_response = f"Desculpe, tive um problema tecnico. Tente novamente. (erro: {e})"
            container.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
    # Só mostra botões após 2 trocas (4 mensagens: 2 do user + 2 do Nino)
    num_msgs = len(st.session_state.messages)
    st.session_state.aguardando_acao = num_msgs >= 4
    st.rerun()
