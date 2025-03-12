from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base


class PedidoPizzaModel(Base):
    __tablename__ = "pedido_pizza"
    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)

    pedido_pizza = relationship("PedidoModel", back_populates="pedido")
