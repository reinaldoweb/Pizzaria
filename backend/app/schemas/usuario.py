from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr


class UsuarioBaseSchema(BaseModel):

    nome: str
    email: EmailStr
    data_criacao: datetime
    is_admin: bool

# Para suportar conversão de ORM para Pydantic
    model_config = ConfigDict(from_attributes=True)


class UsuarioCreateSchema(UsuarioBaseSchema):
    senha: str


class UsuarioSchema(UsuarioBaseSchema):
    id: int
    data_criacao: datetime

    model_config = ConfigDict(from_attributes=True)


class UsuarioUpdateSchema(BaseModel):

    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None  # Pode ser atualizado, mas não é obrigatório

    model_config = ConfigDict(from_attributes=True)
