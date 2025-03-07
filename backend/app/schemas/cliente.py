from typing import Optional
from pydantic import BaseModel


class ClienteSchema(BaseModel):
    id: Optional[int] = None
    nome: str
    endereco: str
    telefone: str

    class config:
        from_attributes = True
