from pydantic import BaseModel, ConfigDict
from typing import Optional


class PizzaBaseSchema(BaseModel):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PizzaSchema(PizzaBaseSchema):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    preco: Optional[float] = None
    sabor: Optional[str] = None


class PizzaUpdateSchema(PizzaBaseSchema):
    pass

    model_config = ConfigDict(from_attributes=True)


class PizzaCreateSchema(BaseModel):
    nome: str
    descricao: str
    preco: float
    sabor: str

    model_config = ConfigDict(from_attributes=True)
