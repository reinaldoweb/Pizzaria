"""
Objetivo:
Simmular um clinete inexistente(.first() retorna None)
Garantir que HTTPException com status_code == 404 seja lançado
"""

from app.services.pedido_service import PedidoService
from fastapi import HTTPException
from unittest.mock import MagicMock
import pytest


def test_criar_novo_pedido_cliente_inexistente():
    pedido_data = {
        "pizza_id": 1,
        "quantidade": 2,
        "preco": 30.00,
    }

    # Cria o mocks
    db_mock = MagicMock()

    # Simula o .fistr() retornando None na busca do cliente
    db_mock.query.return_value.filter.return_value.first.side_effect = [None]

    service = PedidoService(db=db_mock, usuario_logado={})

    with pytest.raises(HTTPException) as exc_info:
        service.criar_novo_pedido(pedido_data, cliente_id=999)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Cliente não encontrado"
