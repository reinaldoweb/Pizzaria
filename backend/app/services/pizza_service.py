from typing import Dict, Any, List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.pizza_model import PizzaModel
import logging

logger = logging.getLogger(__name__)


class PizzaService:
    def __init__(self, db: Session):
        self.db = db

    def criar_nova_pizza(self, pizza_data: dict[str, Any]) -> PizzaModel:
        """
        Cria uma nova pizza no sistema.

        Args:
            pizza_data: Dicionário com os dados da pizza a ser criada
        Returns:
            PizzaModel: A pizza criada

        Raises:
            ValueError: Se os dados forem inválidos
            Exception: Para outros erros inesperados
        """

        try:
            # Valida os dados da pizza
            if not pizza_data.get('nome'):
                raise ValueError("Nome é obrigatório")

            if not isinstance(pizza_data.get('preco'),
                              (int, float)) or pizza_data['preco'] <= 0:
                raise ValueError("Preço deve ser um número")
            # Cria a pizza
            nova_pizza = PizzaModel(**pizza_data)
            self.db.add(nova_pizza)
            self.db.commit()
            self.db.refresh(nova_pizza)

            logger.info(f"Pizza criada: {nova_pizza.nome}")
            return nova_pizza

        except ValueError:
            self.db.rollback()
            logger.error(f"Erro ao criar pizza: {pizza_data}")
            raise

    def buscar_pizza_por_id(self, pizza_id: int) -> Optional[PizzaModel]:
        """
        Busca uma pizza pelo seu ID."

        Args:
            pizza_id: ID da pizza a ser buscada

        Returns:
            PizzaModel: A pizza encontrada ou None se não encontrada
        Raises:
            ValueError: Se o ID for inválido

        """
        if pizza_id <= 0:
            error_msg = f"ID inválido: {pizza_id}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        pizza = self.db.query(PizzaModel).filter_by(id=pizza_id).first()

        if not pizza:
            logger.error("Pizza não encontrada")
            raise ValueError("Pizza não encontrada")
        return pizza

    def listar_todas_pizzas(self) -> List[PizzaModel]:

        """
        Busca todas as pizzas no sistema.
        Returns:
            List[PizzaModel]: Uma lista de pizzas
        """
        logger.info("Buscando todas as pizzas")
        return self.db.query(PizzaModel).order_by(PizzaModel.nome).all()


def atualizar_pizza(
        self,
        pizza_id: int,
        pizza_data: Dict[str, Any]) -> PizzaModel:
    """
    Atualiza uma pizza existente no sistema.

    Args:
        pizza_id: ID da pizza a ser atualizada
        pizza_data: Dicionário com os novos dados da pizza

    Returns:
        PizzaModel: A pizza atualizada

    Raises:
        HTTPException:
            - 400 (BAD_REQUEST) para dados inválidos
            - 404 (NOT_FOUND) se pizza não existir
            - 500 (INTERNAL_SERVER_ERROR) para erros inesperados
    """
    try:
        # Validação básica dos dados de entrada
        if not isinstance(pizza_id, int) or pizza_id <= 0:
            raise ValueError("ID da pizza deve ser um número positivo")

        if "nome" in pizza_data and not pizza_data["nome"]:
            raise ValueError("Nome da pizza não pode ser vazio")

        # Busca a pizza pelo ID
        pizza = self.db.query(PizzaModel).filter_by(id=pizza_id).first()
        if not pizza:
            logger.error(f"Pizza não encontrada: ID {pizza_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                  detail="Pizza não encontrada")

        # Atualiza os campos individualmente
        for key, value in pizza_data.items():
            if hasattr(pizza, key):
                if key == "id":
                    logger.warning(
                        f"Tentativa de alterar ID da pizza {pizza_id}")
                    continue
                setattr(pizza, key, value)

        # Validação adicional do modelo antes de commit
        if not pizza.nome:
            raise ValueError("Nome da pizza é obrigatório")

        self.db.commit()
        self.db.refresh(pizza)
        logger.info(f"Pizza atualizada com sucesso: ID {pizza_id}")
        return pizza

    except ValueError as ve:
        self.db.rollback()
        logger.warning(f"Validação falhou: {str(ve)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except HTTPException:
        self.db.rollback()
        raise
    except Exception as e:
        self.db.rollback()
        logger.exception(f"Erro ao atualizar pizza ID {pizza_id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno ao atualizar pizza: {str(e)}",
        )


def deletar_pizza(self, pizza_id: int) -> None:
    """
    Deleta uma pizza existente no sistema.
    Args:
        pizza_id: ID da pizza a ser deletada
    Raises:
        ValueError: Se a pizza não existir
        Exception: Para outros erros inesperados
    """
    # Busca a pizza pelo ID
    pizza_del = self.db.query(PizzaModel).filter_by(id=pizza_id).one_or_none()

    # Verifica se a pizza existe

    if not pizza_del:
        raise ValueError("Pizza não encontrada")
    # Deleta a pizza
    self.db.delete(pizza_del)
    self.db.commit()
    logger.info(f"Pizza deletada: {pizza_del.nome}")
    return {"message": "Pizza deletada com sucesso"}
