from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.cliente_model import ClienteModel
from app.schemas.cliente import (
    ClienteBaseSchema,
    ClienteSchema,
    ClienteCreateSchema,
    ClienteUpdateSchema
    )
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
    Args:
        cliente: Dados do cliente a ser criado.
        db: Sessão do banco de dados.
        usuario_logado: Usuário autenticado.
    Returns:
        ClienteSchema: Dados do cliente criado.
    """
    try:
        service = ClienteService(db)
        cliente_data = cliente.model_dump()
        cliente_criado = service.criar_novo_cliente(
            usuario_logado.id, cliente_data
        )
        return cliente_criado

    except Exception:
        logger.exception("Erro ao tentar cadastrar cliente")
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
def listar_clientes(db: Session = Depends(get_db)):
    """"
    Retorna uma lista de todos os clientes cadastrados no sistema.
    Args:
        db: Sessão do banco de dados
    Returns:
        List[ClienteBaseSchema]: Lista de clientes cadastrados no sistema
    """

    service = ClienteService(db)
    clientes = service.listar_todos_clientes()
    return clientes


@router.get(
    "/{usuario_id}",
    response_model=ClienteBaseSchema,
    status_code=status.HTTP_200_OK,
    summary="Buscar cliente por ID",
    description="Endpoint para buscar um cliente pelo ID",
)
def get_buscar_cliente_por_id(
    usuario_id: int,
    db: Session = Depends(get_db),
   ) -> ClienteModel:

    service = ClienteService(db)
    cliente = service.buscar_cliente_por_id(usuario_id)

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente


@router.patch(
    "/{cliente_id}",
    status_code=status.HTTP_200_OK,
    response_model=ClienteUpdateSchema,
    summary="Atualizar cliente",
    description="Endpoint para atualizar um cliente",
)
def cliente_update(
    cliente_id: int,
    cliente_data: ClienteUpdateSchema,
    db: Session = Depends(get_db),
    usuario_logado=Depends(get_usuario_logado),
):
    """"
    Atualiza um cliente existente.
    Args:
        cliente_id (int): ID do cliente a ser atualizado.
        cliente_up (ClienteUpdateSchema): Dados atualizados do cliente.
        db (Session, optional): Sessão do banco de dados.
    Returns:
        ClienteModel: O cliente atualizado.
    """
    try:
        service = ClienteService(db, usuario_logado)
        dados_para_atualizar = cliente_data.model_dump(exclude_unset=True)
        cliente_atualizado = service.atualizar_cliente(
            cliente_id, dados_para_atualizar)

        if not cliente_atualizado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente com ID {cliente_id} não encontrado.",
                )
        return cliente_atualizado

    except Exception as e:
        logger.exception(f"Erro ao tentar atualizar cliente: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao atualizar cliente",
        )


@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    usuario_logado: dict = Depends(get_usuario_logado)
        ):

    cliente_del = db.query(ClienteModel).filter(
                    ClienteModel.id == cliente_id).first()

    if not cliente_del:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    db.delete(cliente_del)
    db.commit()
    return
