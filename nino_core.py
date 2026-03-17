"""
nino_core.py - Nucleo de inteligencia do Nino
"""

import json
import os
from datetime import datetime
from openai import OpenAI
import config
from base_conhecimento import buscar_solucao, conhecimento_para_prompt
from modo_aprendizado import enriquecer_prompt_com_memoria
from memoria_conhecimento import buscar_conhecimento
from persistencia import MEMORIA_DIR, APRENDIZADO_FILE, inicializar

import httpx
client = OpenAI(
    api_key=config.OPENAI_API_KEY,
    http_client=httpx.Client()
)

# Garante que diretorios existem na inicializacao
inicializar()

CATEGORIAS = {
    "outlook":          ["outlook", "email", "e-mail", "correio", "caixa de entrada"],
    "teams":            ["teams", "reuniao", "videochamada", "camera", "microfone"],
    "sharepoint":       ["sharepoint", "site", "biblioteca", "permissao"],
    "onedrive":         ["onedrive", "sincroniza", "nuvem", "pasta compartilhada"],
    "vpn":              ["vpn", "acesso remoto", "globalprotect", "cisco"],
    "impressora":       ["impressora", "imprimir", "impressao", "scanner", "toner"],
    "hardware":         ["notebook", "computador", "tela", "bateria", "teclado", "mouse", "nao liga", "lento", "travando"],
    "windows":          ["windows", "sistema operacional", "tela azul", "atualizacao", "driver", "bsod"],
    "internet":         ["internet", "rede", "wi-fi", "wifi", "cabo", "sem conexao"],
    "acesso":           ["senha", "login", "mfa", "autenticacao", "bloqueado", "acesso negado"],
    "microsoft365":     ["microsoft 365", "office", "word", "excel", "powerpoint", "licenca"],
    "buscar_usuario":   ["quem e", "quem é", "me fala sobre", "informacoes de", "perfil de"],
    "buscar_documento": ["onde esta", "onde está", "documento de", "politica de", "localizar arquivo"],
    "buscar_depto":     ["quem trabalha na", "equipe da", "diretoria", "departamento", "setor"],
    "outros":           []
}

SAUDACOES = [
    "oi", "ola", "ola!", "oi!", "bom dia", "boa tarde", "boa noite",
    "tudo bem", "tudo bom", "como vai", "oi nino", "ola nino",
    "e ai", "e aí", "hello", "hey", "hi", "obrigado", "obrigada",
    "valeu", "vlw", "thanks", "ok", "certo", "entendi", "blz", "beleza"
]


def classificar_problema(texto):
    texto_lower = texto.lower()
    for categoria, palavras in CATEGORIAS.items():
        if any(p in texto_lower for p in palavras):
            return categoria
    return "outros"


def eh_saudacao(texto):
    t = texto.lower().strip().rstrip("!?.,:;")
    return any(t == s or t.startswith(s + " ") for s in SAUDACOES)


BASE_SYSTEM_PROMPT = f"""Voce e Nino, assistente corporativo da Bravo TI. Voce tem personalidade agradavel, simpatica e profissional.

SOBRE VOCE:
- Voce e esperto, prestativo e um pouco bem-humorado
- Voce conhece bem os sistemas da empresa, os colaboradores e os documentos internos
- Voce responde de forma natural, como um colega de trabalho que entende de TI

VOCE AJUDA COM:
1. Suporte tecnico de TI (sistemas, equipamentos, aplicativos)
2. Informacoes sobre colaboradores, departamentos e organograma
3. Localizar documentos no SharePoint, Teams e OneDrive
4. Base de Conhecimento da empresa (procedimentos, politicas, manuais, FAQ)
5. Agenda e calendario corporativo
6. Qualquer informacao que esteja na sua base de conhecimento

COMO VOCE RESPONDE:
- De forma natural e humana, nunca robotica
- Respostas curtas e diretas (2 a 4 linhas no maximo)
- Use o nome da pessoa quando souber
- Seja simpatico em saudacoes e conversa casual
- Em problemas tecnicos, seja objetivo e use passos numerados
- Se houver CONHECIMENTO INTERNO ou DOCUMENTOS DO SHAREPOINT, use-os para responder naturalmente
- Nunca invente informacoes. Se nao souber, diga: "Hmm, nao tenho essa informacao. Vou acionar nossa equipe!"

SOBRE O QUE VOCE NAO RESPONDE:
- Assuntos completamente fora da empresa e de TI
- Nesses casos diga: "Haha, esse nao e bem meu forte! Sou especialista em TI corporativo. Posso te ajudar com alguma questao tecnica?"

---

{conhecimento_para_prompt()}
"""


def gerar_resposta_stream(mensagens, prompt_usuario="", historico_anterior=None, contexto_sharepoint="", contexto_fluxo=""):
    """Gera resposta com contexto de memoria, conhecimento e SharePoint."""
    system_prompt = BASE_SYSTEM_PROMPT

    if contexto_fluxo:
        system_prompt += "\n\n" + contexto_fluxo

    if contexto_sharepoint:
        system_prompt += "\n\n[DOCUMENTOS DA BASE DE CONHECIMENTO SHAREPOINT]\n" + contexto_sharepoint

    if prompt_usuario:
        memoria_aprendida = enriquecer_prompt_com_memoria(prompt_usuario)
        if memoria_aprendida:
            system_prompt += "\n\n" + memoria_aprendida

    if prompt_usuario:
        resultado = buscar_solucao(prompt_usuario)
        if resultado:
            perguntas = "\n".join(f"- {p}" for p in resultado["perguntas"])
            solucoes  = "\n".join(f"- {s}" for s in resultado["solucoes"])
            system_prompt += (
                f"\n\n[CONTEXTO TECNICO INTERNO]\n"
                f"Problema: {resultado['problema']}\n"
                f"Perguntas uteis:\n{perguntas}\n"
                f"Solucoes:\n{solucoes}"
            )

    if historico_anterior:
        linhas = []
        for h in historico_anterior[-3:]:
            linhas.append(f"- [{h.get('data','')}] {h.get('problema_relatado','?')} | {h.get('status','?')}")
        system_prompt += f"\n\n[HISTORICO ANTERIOR DO USUARIO]\n" + "\n".join(linhas)

    return client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": system_prompt}] + mensagens,
        stream=True,
        temperature=0.6,
        max_tokens=400,
        presence_penalty=0.4,
    )


def gerar_resposta(mensagens, prompt_usuario="", historico_anterior=None, contexto_sharepoint="", contexto_fluxo=""):
    """Versao nao-streaming para uso em webhooks/API."""
    stream = gerar_resposta_stream(
        mensagens=mensagens,
        prompt_usuario=prompt_usuario,
        historico_anterior=historico_anterior,
        contexto_sharepoint=contexto_sharepoint,
        contexto_fluxo=contexto_fluxo,
    )
    return "".join(
        chunk.choices[0].delta.content or ""
        for chunk in stream
    )


def _garantir_diretorio():
    os.makedirs(MEMORIA_DIR, exist_ok=True)


def _caminho_usuario(identificador):
    nome = identificador.replace("@","_").replace(".","_").replace(" ","_")
    return os.path.join(MEMORIA_DIR, f"{nome}.json")


def carregar_historico_usuario(identificador):
    _garantir_diretorio()
    caminho = _caminho_usuario(identificador)
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"identificador": identificador, "atendimentos": []}


def salvar_atendimento(identificador, conversa, categoria, problema_relatado, status, avaliacao=None):
    _garantir_diretorio()
    dados = carregar_historico_usuario(identificador)
    atendimento = {
        "id":                len(dados["atendimentos"]) + 1,
        "data":              datetime.now().strftime("%Y-%m-%d %H:%M"),
        "problema_relatado": problema_relatado,
        "categoria":         categoria,
        "status":            status,
        "avaliacao":         avaliacao,
        "conversa":          conversa
    }
    dados["atendimentos"].append(atendimento)
    dados["ultimo_atendimento"] = atendimento["data"]
    dados["total_atendimentos"] = len(dados["atendimentos"])
    tmp = _caminho_usuario(identificador) + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    os.replace(tmp, _caminho_usuario(identificador))
    return atendimento


def atualizar_avaliacao(identificador, avaliacao):
    dados = carregar_historico_usuario(identificador)
    if dados["atendimentos"]:
        dados["atendimentos"][-1]["avaliacao"] = avaliacao
        tmp = _caminho_usuario(identificador) + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        os.replace(tmp, _caminho_usuario(identificador))


def tem_historico_recente(identificador, horas=48):
    dados = carregar_historico_usuario(identificador)
    recentes = []
    for a in dados["atendimentos"]:
        try:
            dt = datetime.strptime(a["data"], "%Y-%m-%d %H:%M")
            delta = (datetime.now() - dt).total_seconds() / 3600
            if delta <= horas:
                recentes.append(a)
        except Exception:
            pass
    return recentes


def carregar_todas_metricas():
    _garantir_diretorio()
    metricas = {
        "total_atendimentos": 0,
        "resolvidos":         0,
        "escalados":          0,
        "avaliacoes":         [],
        "categorias":         {},
        "problemas":          [],
        "por_dia":            {},
        "usuarios_unicos":    0
    }
    arquivos = [f for f in os.listdir(MEMORIA_DIR) if f.endswith(".json")]
    metricas["usuarios_unicos"] = len(arquivos)
    for arquivo in arquivos:
        with open(os.path.join(MEMORIA_DIR, arquivo), "r", encoding="utf-8") as f:
            dados = json.load(f)
        for a in dados.get("atendimentos", []):
            metricas["total_atendimentos"] += 1
            if a.get("status") == "resolvido":
                metricas["resolvidos"] += 1
            elif a.get("status") == "escalado":
                metricas["escalados"] += 1
            if a.get("avaliacao"):
                metricas["avaliacoes"].append(a["avaliacao"])
            cat = a.get("categoria", "outros")
            metricas["categorias"][cat] = metricas["categorias"].get(cat, 0) + 1
            if a.get("problema_relatado"):
                metricas["problemas"].append(a["problema_relatado"])
            data = a.get("data", "")[:10]
            if data:
                metricas["por_dia"][data] = metricas["por_dia"].get(data, 0) + 1

    total = metricas["total_atendimentos"]
    metricas["taxa_resolucao"] = round(metricas["resolvidos"] / total * 100, 1) if total > 0 else 0
    avals = metricas["avaliacoes"]
    metricas["media_avaliacao"] = round(sum(avals) / len(avals), 1) if avals else 0
    return metricas


def registrar_solucao_tecnico(problema, categoria, solucao, tecnico=""):
    dados = []
    if os.path.exists(APRENDIZADO_FILE):
        with open(APRENDIZADO_FILE, "r", encoding="utf-8") as f:
            dados = json.load(f)
    dados.append({
        "data":        datetime.now().strftime("%Y-%m-%d %H:%M"),
        "problema":    problema,
        "categoria":   categoria,
        "solucao":     solucao,
        "tecnico":     tecnico,
        "incorporado": False
    })
    tmp = APRENDIZADO_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    os.replace(tmp, APRENDIZADO_FILE)


def listar_solucoes_pendentes():
    if not os.path.exists(APRENDIZADO_FILE):
        return []
    with open(APRENDIZADO_FILE, "r", encoding="utf-8") as f:
        dados = json.load(f)
    return [d for d in dados if not d.get("incorporado")]
