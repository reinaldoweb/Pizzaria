"""
Obejtivo do teste:
Garantir que, quando fornecemos dados válidos:
1- O cliente e a pizza existem
2- O pedido seja criado corretamente
3- O metodo retona um objeto PedidooModel
"""

from app.services.pedido_service import PedidoService
from unittest.mock import MagicMock, patch


def test_criar_novo_pedido_valido():

    pedido_data = {
        "pizza_id": 1,
        "quantidade": 2,
        "preco": 30.00,
    }

    # Cria o mocks
    db_mock = MagicMock()
    cliente_mock = {id: 1}
    pizza_mock = MagicMock(id=1)

    # Simula o retorno de .query().filter().first()
    # Primeiro retorna o cliente, depois a pizza
    db_mock.query.return_value.filter.return_value.first.side_effect = [
        cliente_mock,
        pizza_mock
    ]

    # Simula o comportamento do commit e refresh (sem fazer nada)
    db_mock.commit.return_value = None
    db_mock.refresh.return_value = None

    # Cria instancia de serviço
    service = PedidoService(db=db_mock, usuario_logado={})

    # Executa o método com os mocks
    with patch("app.services.pedido_service.PedidoModel") as PedidoModelMock:
        pedido_instancia_mock = MagicMock()
        PedidoModelMock.return_value = pedido_instancia_mock

        resultado = service.criar_novo_pedido(pedido_data, cliente_id=10)

        PedidoModelMock.assert_called_once_with(
            cliente_id=10,
            pizza_id=1,
            quantidade=2,
            preco=60.00,
            status="pendente"
        )

        assert resultado == pedido_instancia_mock
