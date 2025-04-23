from unittest.mock import MagicMock
from backend.app.services.pedido_service import PedidoService


def test_atualizar_status_para_entregue_como_dono():
    # 1. Criar pedido_mock com cliente_id = 10 e status = "pendente"
    pedido_mock = MagicMock()
    pedido_mock.cliente_id = 10
    pedido_mock.status = "pendente"

    # 2. Criar usuario_logado com id=10, is_admin=False  (é o dono!)
    usuario_logado = {"id": 10, "is_admin": False}

    # 3. Criar db_mock que retorna o pedido
    db_mock = MagicMock()
    db_mock.query.return_value.filter.return_value.first.return_value = pedido_mock

    # 4. Instanciar PedidoService
    service = PedidoService(db_mock, usuario_logado)

    # 5. Chamar atualizar_status(pedido_id, "entregue")
    service.atualizar_status(pedido_id=1, status_novo="entregue")

    # 6. Verificar que status foi atualizado e commit chamado
    assert pedido_mock.status == "entregue"
    db_mock.commit.assert_called_once()
