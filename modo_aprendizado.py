"""
modo_aprendizado.py - Modulo de aprendizado do Nino
"""

from memoria_conhecimento import (
    salvar_conhecimento,
    buscar_conhecimento,
    remover_conhecimento,
    total_conhecimentos,
    listar_conhecimentos,
)


def enriquecer_prompt_com_memoria(pergunta):
    """Busca conhecimentos relevantes e retorna contexto para o prompt."""
    relevantes = buscar_conhecimento(pergunta)
    if not relevantes:
        return ""
    linhas = ["[CONHECIMENTO INTERNO - USE COMO BASE PARA SUA RESPOSTA]"]
    for item in relevantes[:3]:
        linhas.append("- " + item["informacao"])
    return "\n".join(linhas)


def detectar_comando_aprendizado(texto):
    """Verifica se o texto e um comando de aprendizado."""
    t = texto.lower().strip()
    if any(c in t for c in ["nino parar", "encerrar aprendizado", "parar aprendizado"]):
        return "encerrar"
    if any(c in t for c in ["nino aprender", "ativar aprendizado", "modo aprendizado"]):
        return "ativar"
    if "nino listar" in t or "nino ver conhecimento" in t:
        return "listar"
    if "nino remover" in t or "nino deletar" in t:
        return "remover"
    return None


def processar_aprendizado(texto, usuario_id="administrador"):
    entrada = salvar_conhecimento(informacao=texto, ensinado_por=usuario_id)
    total = total_conhecimentos()
    return f"Anotado! Aprendi isso. Total na base: **{total}** registros."


def processar_listar():
    conhecimentos = listar_conhecimentos()
    if not conhecimentos:
        return "Ainda nao tenho nenhum conhecimento armazenado."
    linhas = ["Ultimos conhecimentos:\n"]
    for item in conhecimentos[-10:]:
        linhas.append(f"**[{item['id']}]** ({item.get('categoria','geral')}) — {item['informacao'][:100]}...")
    return "\n".join(linhas)


def processar_remover(texto):
    import re
    numeros = re.findall(r"\d+", texto)
    if not numeros:
        return "Me informe o numero do conhecimento que deseja remover."
    sucesso = remover_conhecimento(int(numeros[0]))
    return f"Conhecimento #{numeros[0]} removido!" if sucesso else "Nao encontrei."
