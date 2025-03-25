from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class PedidoModel(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, default="pendente")
    data_pedido = Column(DateTime, nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    pizza_id = Column(Integer, ForeignKey("pizzas.id"), nullable=False)

    # Relacionamentos
    # Um pedido pertence a um cliente
    clientes = relationship("ClienteModel", back_populates="pedidos")
    # Um pedido pertence a uma pizza
    pizza = relationship("PizzaModel", back_populates="pedidos")
