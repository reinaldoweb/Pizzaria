from pydantic import BaseModel, Field
from typing import Optional


class UsuarioSchema(BaseModel):
    id: Optional[int] = Field(default=None)
    nome: str
    email: str
    senha_hash: str
    data_criacao: str
    is_admin: bool

    class Config:
        from_attributes = True
