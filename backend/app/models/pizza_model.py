from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.core.database import Base


class PizzaModel(Base):
    __tablename__ = "pizzas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=True)
    descricao = Column(String(255), nullable=True)
    preco = Column(Float, nullable=True)
    sabor = Column(String(255), nullable=True)

    pedido_pizza = relationship("PedidoModel", back_populates="pizza_pedido")
