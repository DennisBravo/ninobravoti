"""
graph_service.py - Servico que consolida buscas no Microsoft Graph
"""

from graph_client import buscar_usuario, buscar_documento, listar_departamentos


def consultar_graph(tipo, termo=""):
    """
    Consulta o Graph conforme o tipo: usuario, documento ou departamento.
    Retorna texto formatado para o prompt do Nino.
    """
    if tipo == "usuario":
        usuarios = buscar_usuario(termo)
        if not usuarios:
            return ""
        linhas = ["[USUARIOS ENCONTRADOS]"]
        for u in usuarios[:5]:
            nome = u.get("displayName", u.get("nome", "?"))
            email = u.get("mail", u.get("email", ""))
            linhas.append(f"- {nome} ({email})" if email else f"- {nome}")
        return "\n".join(linhas)

    if tipo == "documento":
        docs = buscar_documento(termo)
        if not docs:
            return ""
        linhas = ["[DOCUMENTOS ENCONTRADOS]"]
        for d in docs[:5]:
            titulo = d.get("name", d.get("titulo", "?"))
            url = d.get("webUrl", d.get("url", ""))
            linhas.append(f"- {titulo}" + (f" | {url}" if url else ""))
        return "\n".join(linhas)

    if tipo == "departamento":
        deptos = listar_departamentos()
        if not deptos:
            return ""
        linhas = ["[DEPARTAMENTOS]"]
        for d in deptos[:10]:
            nome = d.get("displayName", d.get("nome", "?"))
            linhas.append(f"- {nome}")
        return "\n".join(linhas)

    return ""
