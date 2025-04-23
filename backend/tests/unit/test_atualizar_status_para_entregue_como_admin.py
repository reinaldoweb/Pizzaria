"""
Objetivo do teste:
1- Quando o pedido é encontrado
2- O método alterar_status_pedido()
3 - altera o status do pedido para "Entregue"
"""

from unittest.mock import MagicMock
from app.services.pedido_service import PedidoService


def test_atualizar_status_para_entregue_como_admin():
    # 1. Criar pedido_mock com cliente_id = 10 e status = "pendente"
    pedido_mock = MagicMock()
    pedido_mock.cliente_id = 10
    pedido_mock.status = "pendente"
    # 2. Criar usuario_logado com is_admin=True
    usuario_logado = {"id": 99, "is_admin": True}
    # 3. Criar db_mock que retorna o pedido
    db_mock = MagicMock()
    db_mock_query = db_mock.query.return_value
    db_mock_filter = db_mock_query.filter.return_value
    db_mock_filter.first.return_value = pedido_mock
    # 4. Instanciar PedidoService com usuario_logado
    service = PedidoService(db_mock, usuario_logado)
    # 5. Chamar atualizar_status(pedido_id, "entregue")
    service.atualizar_status(1, "entregue")
    # 6. Verificar que status foi atualizado para "entregue"
    assert pedido_mock.status == "entregue"
    db_mock.commit.assert_called_once()
