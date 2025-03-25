from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String
from app.core.database import Base


class ClienteModel(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=True)
    nome = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    endereco = Column(String, nullable=False)

    # Relacionamentos
    # Um cliente pertence a um usuário
    usuario = relationship("UsuarioModel", back_populates="cliente")
    # Um cliente pode ter vários pedidos
    pedidos = relationship("PedidoModel", back_populates="clientes")
