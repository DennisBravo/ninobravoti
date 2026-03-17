"""
graph_client.py - Integracao com Microsoft Graph API
Busca usuarios, documentos e departamentos.
"""

import asyncio


async def buscar_usuario(termo):
    """
    Busca usuario no Microsoft Graph pelo nome ou email.
    Retorna string formatada ou None.
    """
    # Stub: integracao real com Graph API
    return None


async def buscar_documento(termo):
    """
    Busca documento no SharePoint/OneDrive pelo termo.
    Retorna string formatada ou None.
    """
    # Stub: integracao real com Graph API
    return None


async def listar_departamento(termo):
    """
    Lista departamentos ou pessoas de um departamento.
    Retorna string formatada ou None.
    """
    # Stub: integracao real com Graph API
    return None


# Alias para compatibilidade (graph_service pode importar listar_departam)
listar_departam = listar_departamento
