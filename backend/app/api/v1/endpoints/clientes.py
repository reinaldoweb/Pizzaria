from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.cliente_model import ClienteModel
from app.schemas.cliente import (
    ClienteBaseSchema,
    ClienteSchema,
    ClienteCreateSchema)
from app.core.database import get_db
from app.core.dependencies import get_current_user as get_usuario_logado
from app.services.cliente_service import ClienteService

import logging
logger = logging.getLogger(__name__)

# Definindo a rota de criação de clientes
router = APIRouter()


@router.post("/",
             response_model=ClienteSchema,
             summary="Cria um novo cliente",
             description="Endpoint para criar um novo cliente no sistema",
             status_code=status.HTTP_201_CREATED
             )
def criar_cliente(
        cliente: ClienteCreateSchema,
        db: Session = Depends(get_db),
        usuario_logado=Depends(get_usuario_logado),
) -> ClienteSchema:
    """
    Cria um novo cliente para o usuário autenticado.
    :param cliente: Dados do cliente a ser criado (schema de criação)
    :param db: Sessão do banco de dados
    :param usuario_logado: Usuário autenticado
    :return: ClienteSchema: O cliente criado com seus dados
    """
    try:
        service = ClienteService(db)
        cliente_data = cliente.model_dump()
        cliente_criado = service.criar_novo_cliente(
            usuario_id=usuario_logado.id, cliente_data=cliente_data
            )
        return cliente_criado
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e))
    except Exception as e:
        logger.exception(f"Erro ao tentar cadastrar cliente: {str(e)}")
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao cadastrar cliente",
        )
    raise


@router.get("/",
            response_model=List[ClienteBaseSchema],
            status_code=status.HTTP_200_OK,
            summary="Listar todos os clientes",
            description="Endpoint para listar todos os clientes"
            "cadastrados no sistema"
            )
def listar_clientes(
    db: Session = Depends(get_db)
) -> List[ClienteBaseSchema]:
    """"
    Retorna uma lista de todos os clientes cadastrados no sistema.
    :param db: Sessão do banco de dados
    :return: List[ClienteBaseSchema]:
    Uma lista de todos os clientes cadastrados
    """
    try:
        service = ClienteService(db)
        logger.info("Listando todos os clientes")
        return service.listar_todos_clientes()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao carregar Lista de clientes.")
    except Exception:
        logger.exception("Erro ao tentar listar clientes.")
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao listar clientes",
        )
    raise


@router.get(
    "/{cliente_id}",
    response_model=ClienteSchema,
    status_code=status.HTTP_200_OK,
)
async def buscar_cliente_por_id(cliente_id: int,
                                db: Session = Depends(get_db)):
    cliente_id = (
        db.query(ClienteModel).filter(
            ClienteModel.id == cliente_id).one_or_none()
    )
    if not cliente_id:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente_id


@router.patch(
    "/{cliente_id}",
    response_model=ClienteSchema,
    status_code=status.HTTP_200_OK,
)
def cliente_update(
    cliente_id: int,
    cliente_up: ClienteBaseSchema,
    db: Session = Depends(get_db),
) -> ClienteBaseSchema:

    # Busca o cliente no banco de dados

    cliente_db = db.query(ClienteModel).filter(
        ClienteModel.id == cliente_id).first()

    # Verifica se o cliente existe

    if not cliente_db:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    # Atualliza apenas os campos que foram fornecdidos no payload

    cliente_update = cliente_up.model_dump(exclude_unset=True)

    for field, value in cliente_update.items():
        setattr(cliente_db, field, value)

    try:
        db.commit()
        db.refresh(cliente_db)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar pedido: {str(e)}",
        )

    return cliente_db


@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente_del = (
        db.query(ClienteModel).filter(
            ClienteModel.id == cliente_id).one_or_none()
    )
    if not cliente_del:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    db.delete(cliente_del)
    db.commit()
    return {"message": "Cliente deletado com sucesso"}
