from sqlalchemy import Column, Integer, String
from app.core.database import Base


class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)
    data_criacao = Column(String(20), nullable=False)
    # "admin" ou "cliente"
    tipo = Column(String(50), nullable=False)
