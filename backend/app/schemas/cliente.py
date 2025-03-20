from typing import Optional
from pydantic import BaseModel


class ClienteBaseSchema(BaseModel):

    nome: str
    endereco: str
    telefone: str

    class config:
        from_attributes = True


class ClienteCreateSchema(ClienteBaseSchema):
    nome: str
    endereco: str
    telefone: str


class ClienteSchema(BaseModel):
    id: Optional[int] = None

    class Config:
        from_attributes = True


class ClienteUpdateSchema(BaseModel):
    nome: Optional[str] = None
    endereco: Optional[str] = None
    telefone: Optional[str] = None

    class Config:
        from_attributes = True
