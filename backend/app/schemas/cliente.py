from typing import Optional
from pydantic import BaseModel, ConfigDict


class ClienteBaseSchema(BaseModel):
    nome: str
    endereco: str
    telefone: str

    class Config:
        # ou orm_mode=True se estiver usando Pydantic v1
        from_attributes = True


class ClienteCreateSchema(ClienteBaseSchema):
    pass  # Herda tudo de ClienteBaseSchema, não precisa repetir os campos


class ClienteUpdateSchema(BaseModel):
    nome: Optional[str] = None
    endereco: Optional[str] = None
    telefone: Optional[str] = None

    class Config:
        from_attributes = True


class ClienteSchema(ClienteBaseSchema):
    id: int  # Nesse caso, o ID é obrigatório na resposta

    model_config = ConfigDict(from_attributes=True)
