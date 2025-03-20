from pydantic import BaseModel


class PedidoBaseSchema(BaseModel):
    cliente_id: int
    status: str

    class config:
        from_attributes = True


class PedidoSchema(PedidoBaseSchema):
    data_pedido: str


class PedidoCreateSchema(PedidoSchema):
    id: int
    pedido_pizza_id: int

    class Config:
        from_attributes = True
