from sqlalchemy import Column, DateTime, Integer, String
from app.core.database import Base


class PedidoModel(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, default="pendente")
    data_pedido = Column(DateTime, nullable=False)
    cliente_id = Column(Integer, nullable=False)
    pedido_pizza_id = Column(Integer, nullable=False)
