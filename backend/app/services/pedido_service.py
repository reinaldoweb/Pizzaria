import logging
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.pedido_model import PedidoModel
from app.models.pizza_model import PizzaModel
from app.models.cliente_model import ClienteModel

logger = logging.getLogger(__name__)


class PedidoService:
    def __init__(self, db: Session, usuario_logado: dict):
        self.db = db
        self.usuario_logado = usuario_logado

    def criar_novo_pedido(
            self, pedido_data: dict, cliente_id: int) -> PedidoModel:
        preco_total = self.calcular_pedido(
            pedido_data["preco"], pedido_data["quantidade"]
        )
        # Verifica se o cliente existe
        cliente = self._buscar_cliente(cliente_id)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente não encontrado",
            )
        # Verifica se a pizza existe
        pizza = self._buscar_pizza(pedido_data["pizza_id"])
        if not pizza:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pizza não encontrada",
            )

        try:
            novo_pedido = PedidoModel(
                cliente_id=cliente_id,
                pizza_id=pedido_data["pizza_id"],
                quantidade=pedido_data["quantidade"],
                preco=preco_total,
                status="pendente",
            )

            self.db.add(novo_pedido)
            self.db.commit()
            self.db.refresh(novo_pedido)
            logger.info(f"Pedido criado: {novo_pedido.id}")
            return novo_pedido

        except Exception:
            self.db.rollback()
            logger.exception("Erro ao criar pedido")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao criar pedido",
            )

    def calcular_pedido(self, preco: float, quantidade: int) -> float:
        try:
            return preco * quantidade
        except Exception as e:
            logger.error(f"Erro ao calcular pedido: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao calcular pedido",
            )

    # Função privada para buscar o cliente e a pizza
    def _buscar_cliente(self, cliente_id: int) -> ClienteModel:
        cliente = (
            self.db.query(
                ClienteModel).filter(ClienteModel.id == cliente_id).first()
        )
        if not cliente:
            logger.error(f"Cliente não encontrado: {cliente_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente não encontrado"
            )
        return cliente

    # Função privada para buscar a pizza
    def _buscar_pizza(self, pizza_id: int) -> PizzaModel:
        pizza = self.db.query(
            PizzaModel).filter(PizzaModel.id == pizza_id).first()
        if not pizza:
            logger.error(f"Pizza não encontrada: {pizza_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                  detail="Pizza não encontrada")
        return pizza


def delete_pizza(self, pizza_id: int) -> None:
    try:
        pizza_delete = self.db.query(PizzaModel).filter(
            PizzaModel.id == pizza_id).first()
        if not pizza_delete:
            logger.error(f"Pizza não encontrada: {pizza_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pizza não encontrada"
            )
        self.db.delete(pizza_delete)
        self.db.commit()
        logger.info(f"Pizza deletada com sucesso!: {pizza_id}")
        return {"message": "Pizza deletada com sucesso!"}
    except Exception:
        self.db.rollback()
        logger.exception("Erro ao deletar pizza")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao deletar pizza"
        )
