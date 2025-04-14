from app.services.pedido_service import PedidoService


def test_calcular_pedido_valido():
    db_mock = None
    usuario_mock = {"id": 1}
    service = PedidoService(db_mock, usuario_mock)

    preco = 30.00
    quantidade = 2

    resultado = service.calcular_pedido(preco, quantidade)
    assert resultado == 60.00, "O cálculo do total do pedido está incorreto"
