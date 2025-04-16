"""
Objetivo: Testar se o sistema retorna uma mensagem de erro quando os dados do
pedido são inválidos.

"""

from app.services.pedido_service import PedidoService
from fastapi import HTTPException
import pytest


def test_calcular_pedido_dados_invalido():
    # 1. Instanciar PedidoService com db e usuario fake
    PedidoServiceFake = PedidoService(db=None, usuario_logado={})

    # 2. Chamar calcular_pedido com preco=None e quantidade válida
    with pytest.raises(HTTPException) as exc_info:
        PedidoServiceFake.calcular_pedido(preco=None, quantidade=1)

    # 3. Capturar a HTTPException e verificar se:
    #    - status_code == 400
    #    - detail == "Erro ao calcular pedido"
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Erro ao calcular pedido"
