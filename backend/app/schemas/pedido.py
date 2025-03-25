from datetime import datetime
from pydantic import BaseModel


class PedidoBaseSchema(BaseModel):
    id: int

    class config:
        from_attributes = True


class PedidoSchema(PedidoBaseSchema):
    pass


class PedidoCreateSchema(BaseModel):
    cliente_id: int
    pizza_id: int
    status: str
    data_pedido: datetime

    class Config:
        from_attributes = True
