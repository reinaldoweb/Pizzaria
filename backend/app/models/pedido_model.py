from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class PedidoModel(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, default="pendente")
    data_pedido = Column(DateTime, nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    pedido_pizza_id = Column(Integer, nullable=False)

    cliente = relationship("ClienteModel", back_populates="pedidos")
    pedido_pizza = relationship("PedidoPizzaModel", back_populates="pedido")
