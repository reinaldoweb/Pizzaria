from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    data_criacao = Column(DateTime, default=datetime.now(), nullable=False)
    # "admin" ou "cliente"
    is_admin = Column(Boolean, default=False, nullable=False)

    cliente = relationship("ClienteModel", back_populates="usuario")
