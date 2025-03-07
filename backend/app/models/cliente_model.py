from sqlalchemy import Column, Integer, String
from app.core.database import Base
from sqlalchemy.orm import relationship


class ClienteModel(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    endereco = Column(String, nullable=False)

    # Verifique se a relação está definida corretamente
    pedidos = relationship("PedidoModel", back_populates="cliente")
    usuarios = relationship("UsuarioModel", back_populates="cliente")
