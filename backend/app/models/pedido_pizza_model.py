from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class PedidoPizzaModel(Base):
    __tablename__ = "pedido_pizza"
    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedido.id"))
    pizza_id = Column(Integer, ForeignKey("pizza.id"))
    quantidade = Column(Integer, nullable=False)

    pedido_id = relationship("PedidoModel", back_populates="pedido_pizzas")
    pizza_id = relationship("PizzaModel", back_populates="pedido_pizzas")
