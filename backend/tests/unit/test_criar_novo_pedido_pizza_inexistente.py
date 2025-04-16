"""
Objetivo do teste:
1- Quando a pízza não é encontrada(. first() retorna None)
2- O método criar_novo_pedido()
lança uma HTTPException com status_code == 404
detalhe: "Pizza não encontrada"
"""

from app.services.pedido_service import PedidoService
from fastapi import HTTPException
from unittest.mock import MagicMock
import pytest
from app.models.cliente_model import ClienteModel
from app.models.pizza_model import PizzaModel


def test_criar_novo_pedido_pizza_inexistente():
    pedido_data = {
        "pizza_id": 10,
        "quantidade": 2,
        "preco": 30.00,
    }

    # Mocks de cliente e pizza
    cliente_mock = MagicMock(id=10)

    # Mock do db.query com comportamento diferente por modelo
    def mock_query(model):
        query_mock = MagicMock()
        if model == ClienteModel:
            query_mock.filter.return_value.first.return_value = cliente_mock
        elif model == PizzaModel:
            query_mock.filter.return_value.first.return_value = None
        return query_mock

    db_mock = MagicMock()
    db_mock.query.side_effect = mock_query

    service = PedidoService(db=db_mock, usuario_logado={})

    with pytest.raises(HTTPException) as exc_info:
        service.criar_novo_pedido(pedido_data, cliente_id=1)

    # Verifica se a exceção foi lançada com os detalhes corretos
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Pizza não encontrada"
