from pydantic import BaseModel
from typing import Optional


class PizzaBaseSchema(BaseModel):
    id: int

    class Config:
        # Certifique-se de que está corretamente capitalizado
        from_attributes = True


class PizzaSchema(PizzaBaseSchema):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    preco: Optional[float] = None
    sabor: Optional[str] = None


class PizzaUpdateSchema(PizzaBaseSchema):
    pass

    class Config:
        # Garantindo que Pydantic reconheça atributos ORM
        from_attributes = True


class PizzaCreateSchema(BaseModel):
    nome: str
    descricao: str
    preco: float
    sabor: str

    class Config:
        # Mantendo compatibilidade com Pydantic ORM
        from_attributes = True
