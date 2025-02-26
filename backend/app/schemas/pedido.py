from pydantic import BaseModel


class PedidoSchema(BaseModel):
    id_cliente: int
    cliente_id: int
    usuario_id: int
    status: str
    data_pedido: str

    class config:
        from_attributes = True
