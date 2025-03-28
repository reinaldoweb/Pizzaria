from fastapi import HTTPException, status
from app.models.pedido_model import PedidoModel
from app.models.cliente_model import ClienteModel
import logging
from app.models.pizza_model import PizzaModel
from sqlalchemy.orm import Session


logger = logging.getLogger(__name__)


class PedidoService:
    def __init__(self, db: Session, usuario_logado: dict):
        self.db = db


def criar_novo_pedido(
        self, pedido_data: dict, cliente_id: int) -> PedidoModel:
    """Cria um novo pedido no sistema"""
    # Valida se o cliente existe
    cliente = self.db.query(ClienteModel).filter(
        ClienteModel.id == cliente_id).first()
    if not cliente:
        logger.error(f"Cliente não encontrado: {cliente_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )
    # Verifica se a pizza existe
    pizza = self.db.query(PizzaModel).filter_by(
        id=pedido_data['pizza_id']).first()
    if not pizza:
        logger.error(f"Pizza não encontrada: {pedido_data['pizza_id']}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pizza não encontrada"
        )

    try:
        # Calcula o preço do pedido
        preco_total = pedido_data['preco'] * pedido_data['quantidade']

        # Cria o pedido
        novo_pedido = PedidoModel(
            cliente_id=cliente_id,
            pizza_id=pedido_data['pizza_id'],
            quantidade=pedido_data['quantidade'],
            preco=preco_total,
            # status padrão para novo pedido
            status='pendente'
        )
        self.db.add(novo_pedido)
        self.db.commit()
        self.db.refresh(novo_pedido)
        logger.info(f"Pedido criado: {novo_pedido.id}")
        if novo_pedido:
            logger.info(f"Pedido criado com sucesso: {novo_pedido.id}")
            raise HTTPException(
                status_code=status.HTTP_201_CREATED,
                detail="Pedido criado com sucesso!!"
            )
        # Retorna o novo pedido criado
        return novo_pedido
    except Exception:
        self.db.rollback()
        logger.exception("Erro ao criar pedido")
        raise
