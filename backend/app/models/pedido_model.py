from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class PedidoModel(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, default="pendente")
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    pizza_id = Column(Integer, ForeignKey("pizzas.id"), nullable=False)
    data_pedido = Column(DateTime, nullable=False)

    pedido_cliente = relationship("ClienteModel", back_populates="cliente")
    pedidos = relationship("UsuarioModel", back_populates="pedidos_user")
    pizza_pedido = relationship("PizzaModel", back_populates="pedido_pizza")

    pedido = relationship("PedidoPizzaModel", back_populates="pedido_pizza")
