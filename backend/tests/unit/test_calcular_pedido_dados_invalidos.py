"""
Objetivo: Testar se o sistema retorna uma mensagem de erro quando os dados do
pedido são inválidos.

"""

from fastapi import HTTPException
import pytest


def test_calcular_pedido_dados_invalido(pedido_service_mockado):

    service, _ = pedido_service_mockado

    # 2. Chamar calcular_pedido com preco=None e quantidade válida
    with pytest.raises(HTTPException) as exc_info:
        service.calcular_pedido(preco=None, quantidade=1)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Erro ao calcular o pedido."
