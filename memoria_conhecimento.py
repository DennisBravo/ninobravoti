"""
memoria_conhecimento.py - Base de conhecimento aprendido pelo Nino
"""

import json
import os
from datetime import datetime

try:
    from persistencia import CONHECIMENTO_FILE, inicializar
except ImportError:
    _dir = os.path.dirname(os.path.abspath(__file__))
    CONHECIMENTO_FILE = os.path.join(_dir, "base_conhecimento_aprendido.json")
    def inicializar():
        os.makedirs(os.path.dirname(CONHECIMENTO_FILE), exist_ok=True)


def _carregar_base():
    if os.path.exists(CONHECIMENTO_FILE):
        with open(CONHECIMENTO_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"conhecimentos": []}


def _salvar_base(dados):
    tmp = CONHECIMENTO_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    os.replace(tmp, CONHECIMENTO_FILE)


def _detectar_categoria(texto):
    t = texto.lower()
    if any(p in t for p in ["diretor", "gerente", "coordenador", "analista", "cargo"]):
        return "cargo"
    if any(p in t for p in ["empresa", "cnpj", "sede"]):
        return "empresa"
    if any(p in t for p in ["processo", "procedimento", "fluxo"]):
        return "processo"
    if any(p in t for p in ["documento", "arquivo", "contrato"]):
        return "documento"
    if any(p in t for p in ["politica", "regra", "norma"]):
        return "politica"
    if any(p in t for p in ["sistema", "software", "aplicativo"]):
        return "sistema"
    return "geral"


def salvar_conhecimento(informacao, ensinado_por="administrador", categoria=None):
    inicializar()
    dados = _carregar_base()
    cat = categoria or _detectar_categoria(informacao)
    entrada = {
        "id": len(dados["conhecimentos"]) + 1,
        "informacao": informacao,
        "categoria": cat,
        "data": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "ensinado_por": ensinado_por,
        "ativo": True,
    }
    dados["conhecimentos"].append(entrada)
    _salvar_base(dados)
    return entrada


def buscar_conhecimento(termo):
    """Busca conhecimentos relevantes ao termo."""
    dados = _carregar_base()
    termo_lower = termo.lower()
    resultados = []
    for item in dados.get("conhecimentos", []):
        if not item.get("ativo", True):
            continue
        if termo_lower in item.get("informacao", "").lower():
            resultados.append(item)
    return resultados[:5]


def atualizar_conhecimento(id_conhecimento, nova_informacao, atualizado_por="administrador"):
    dados = _carregar_base()
    for item in dados["conhecimentos"]:
        if item["id"] == id_conhecimento:
            item["informacao"] = nova_informacao
            item["atualizado_em"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            _salvar_base(dados)
            return True
    return False


def remover_conhecimento(id_conhecimento):
    dados = _carregar_base()
    for item in dados["conhecimentos"]:
        if item["id"] == id_conhecimento:
            item["ativo"] = False
            _salvar_base(dados)
            return True
    return False


def total_conhecimentos():
    return len([c for c in _carregar_base().get("conhecimentos", []) if c.get("ativo", True)])


def listar_conhecimentos():
    return [c for c in _carregar_base().get("conhecimentos", []) if c.get("ativo", True)]
