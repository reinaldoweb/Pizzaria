from pydantic import BaseModel, Field
from typing import Optional


class PedidoPizzaSchema(BaseModel):
    id: Optional[int] = Field(default=None)
    pedido_id: int
    pizza_id: int
    quantidade: int

    class config:
        from_attributes = True
