from datetime import datetime
from pydantic import BaseModel, ConfigDict


class PedidoBaseSchema(BaseModel):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PedidoSchema(PedidoBaseSchema):
    pass


class PedidoCreateSchema(BaseModel):
    cliente_id: int
    pizza_id: int
    status: str
    data_pedido: datetime

    model_config = ConfigDict(from_attributes=True)
