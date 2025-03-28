from typing import List
from fastapi import APIRouter, logger, status, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.pizza_model import PizzaModel
from app.schemas.pizza import (
    PizzaBaseSchema,
    PizzaCreateSchema,
    PizzaSchema,
    PizzaUpdateSchema
    )
from app.services.pizza_service import PizzaService


router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=PizzaCreateSchema,
    summary="Cria uma nova pizza",
    description="End point para cadastro de pizza no sistema",
)
def create_pizza(
    pizza: PizzaCreateSchema,
    db: Session = Depends(get_db)
) -> PizzaSchema:
    """Cria uma nova pizza no sistema.
    Args:
        pizza: Dados da pizza a ser criada
        db: Sessão do banco de dados
    Returns:
        PizzaModel: A pizza criada com seus dados
    """

    service = PizzaService(db)
    pizza_data = pizza.model_dump()
    pizza_criada = service.criar_nova_pizza(pizza_data)
    if pizza_criada:
        raise HTTPException(
            status_code=status.HTTP_201_CREATED,
            detail="Pizza criada com sucesso"
        )
    logger.info(f"Pizza criada: {pizza_criada.nome}")
    return pizza_criada


@router.get(
    "/",
    response_model=List[PizzaSchema],
    summary="Lista todas as pizzas cadastradas no sistema",
    description="Endpoint para listar todas as pizzas cadastradas",
)
def listar_pizzas(db: Session = Depends(get_db)):
    """
    Lista todas as pizzas cadastradas no sistema.
    Args:
        db: Sessão do banco de dados
    Returns:
        List[PizzaModel]: Lista com todas as pizzas cadastradas
    """
    service = PizzaService(db)
    return service.listar_todas_pizzas()


@router.get(
    "/{pizza_id}",
    status_code=status.HTTP_200_OK,
    response_model=PizzaSchema,
    summary="Busca uma pizza pelo ID",
    description="Endpoint para buscar uma pizza no sistema",
)
def buscar_pizza(
    pizza: PizzaBaseSchema,
    db: Session = Depends(get_db)
) -> PizzaModel:
    """ "
    Busca uma pizza pelo ID.
    Args:
        pizza_id: ID da pizza
        db: Sessão do banco de dados
    Returns:
        PizzaModel: A pizza encontrada com seus dados
    """
    service = PizzaService(db)
    pizza_data = pizza.model_dump()
    return service.buscar_pizza_por_id(**pizza_data)


@router.patch(
    "/{pizza_id}",
    response_model=PizzaSchema,
    status_code=status.HTTP_200_OK,
    summary="Atualiza uma pizza pelo ID",
    description="Endpoint para atualizar uma pizza no sistema",
)
def update_pizza(
    pizza_id: int,
    pizza_data: PizzaUpdateSchema,
    db: Session = Depends(get_db)
):

    """
        Atualiza os dados de uma pizza existente.

        Args:
            pizza_id: ID da pizza a ser atualizada
            pizza_data: Dados de atualização da pizza (schema)
            db: Sessão do banco de dados

        Returns:
            PizzaResponseSchema: Pizza atualizada com todos os dados

        Raises:
            HTTPException 400: Se os dados forem inválidos
            HTTPException 404: Se a pizza não for encontrada
            HTTPException 500: Erro interno no servidor
        """
    try:
        service = PizzaService(db)
        pizza_data = pizza_data.model_dump(exclude_unset=True)
        pizza_atualizada = service.atualizar_pizza(pizza_id, pizza_data)
        return pizza_atualizada
    except Exception:
        raise

    except Exception as e:
        logger.error(f"Erro não tratado ao atualizar pizza: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
              detail="Ocorreu um erro inseperado ao atualizar a pizza.")


@router.delete(
    "/{pizza_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deleta uma pizza pelo ID",
    description="Endpoint para deletar uma pizza no sistema",
)
def delete_pizza(id: int, db: Session = Depends(get_db)):
    pizza = db.query(PizzaModel).filter(PizzaModel.id == id).first()
    if pizza is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pizza não encontrada!"
        )
    db.delete(pizza)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
