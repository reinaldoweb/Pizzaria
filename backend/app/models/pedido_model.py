from sqlalchemy import Column, DateTime, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class PedidoModel(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    status = Column(String, default="pendente")
    data_pedido = Column(DateTime, nullable=False)

# Relacionamento com a tabela de clientes
    usuario = relationship("UsuarioModel", back_populates="pedidos")
    cliente = relationship("ClienteModel", back_populates="pedidos")
