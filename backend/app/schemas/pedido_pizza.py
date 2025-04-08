from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class PedidoPizzaSchema(BaseModel):
    id: Optional[int] = Field(default=None)
    pedido_id: int
    pizza_id: int
    quantidade: int

    model_config = ConfigDict(from_attributes=True)
