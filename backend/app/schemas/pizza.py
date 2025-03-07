from pydantic import BaseModel

from typing import Optional


class PizzaSchema(BaseModel):
    id: Optional[int] = None
    nome: str
    descricao: str
    preco: float
    sabor: str

    class Config:
        from_attributes = True
