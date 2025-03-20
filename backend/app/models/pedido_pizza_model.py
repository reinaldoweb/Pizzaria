from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from app.core.database import Base


class PedidoPizzaModel(Base):
    __tablename__ = "pedido_pizza"
    id = Column(Integer, primary_key=True, index=True)
    quantidade = Column(Integer, nullable=False)
    pizza_id = Column(Integer, nullable=False)

    pedido = relationship("PedidoModel", back_populates="pedido_pizza")
