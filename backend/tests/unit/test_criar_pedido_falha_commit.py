"""
Objetivo: Testar a falha do banco de dados.
Garantir que:
- A transação seja revertida em caso de falha(db.rollback() é chamado).
- Uma exceção é lançada quando a transação é revertida. com a mensagem de erro.
"Erro ao criar o pedido".
"""

import pytest
from unittest.mock import MagicMock
from app.services.pedido_service import PedidoService
from fastapi import HTTPException

from app.models.cliente_model import ClienteModel
from app.models.pizza_model import PizzaModel


def test_criar_pedido_falha_commit():
    # 1. Criar dados de pedido válidos (pizza_id, quantidade, preco)
    pedido_data = {
        "pizza_id": 1,
        "quantidade": 2,
        "preco": 30.0,
    }

    # 2. Criar mocks:
    # cliente_mock
    cliente_mock = MagicMock(id=1)
    # pizza_mock
    pizza_mock = MagicMock(id=1)

    def mock_query(model):
        q = MagicMock()
        if model is ClienteModel:
            q.filter.return_value.firts.return_value = cliente_mock
        elif model is PizzaModel:
            q.filter.return_value.firts.return_value = pizza_mock
        return q

    # 3. Criar db_mock com:
    db_mock = MagicMock()
    # .query().filter().first() -> side_effect = [cliente_mock, pizza_mock]
    db_mock.query.side_effect = mock_query
    # .commit() -> lançar exceção (ex: Exception("Erro no banco"))
    db_mock.commit().side_effect = Exception("Erro no banco")
    db_mock.refresh = MagicMock()

    # 4. Criar instância de PedidoService
    service = PedidoService(db=db_mock, usuario_logado={})

    # 5. Chamar criar_novo_pedido e capturar com pytest.raises(HTTPException)
    with pytest.raises(HTTPException) as exc_info:
        service.criar_novo_pedido(pedido_data, cliente_id=1)

    # 6. Verificar se:

    # db.rollback foi chamado
    db_mock.rollback.assert_called_once()
    # status_code == 500
    assert exc_info.value.status_code == 500
    # detail == "Erro ao criar pedido"
    assert exc_info.value.detail == "Erro ao criar pedido"
