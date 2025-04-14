from typing import Annotated, List, Union
from fastapi import APIRouter, Depends, HTTPException, logger, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.usuario_model import UsuarioModel
from app.schemas.usuario import (UsuarioBaseSchema, UsuarioSchema,
                                 UsuarioCreateSchema, UsuarioUpdateSchema)
from app.core.dependencies import get_current_active_user

from app.services.usuario_service import UsuarioService
from app.core.security import gerar_hash_senha
import logging


router = APIRouter()


@router.post(
    "/",
    response_model=UsuarioSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo usuário",
    description="Endpoint para cadastrar um novo usuário no sistema",
)
def create_usuario(
    usuario: UsuarioCreateSchema,
    db: Session = Depends(get_db)
) -> UsuarioSchema:
    """
    Cria um novo usuário no sistema.

    Args:
        usuario: Dados do usuário a ser criado (schema de criação)
        db: Sessão do banco de dados

    Returns:
        UsuarioSchema: O usuário criado com seus dados

    Raises:
        HTTPException: 400 se o e-mail já estiver cadastrado
        HTTPException: 500 em caso de erro interno
    """
    try:
        service = UsuarioService(db)
        usuario_data = usuario.model_dump()

        # Se o schema inclui senha diretamente (não hash)
        if "senha" in usuario_data:
            usuario_data["senha_hash"] = gerar_hash_senha(
                usuario_data.pop("senha"))

        usuario_criado = service.criar_usuario(usuario_data)
        return usuario_criado

    except ValueError as e:
        # Erro de e-mail duplicado
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Erro ao criar usuário: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao criar usuário",
        )


@router.get("/", response_model=List[UsuarioBaseSchema],
            status_code=status.HTTP_200_OK)
def get_usuarios(db: Session = Depends(get_db)):
    return db.query(UsuarioModel).all()


@router.get(
    "/{usuario_id}", response_model=UsuarioBaseSchema,
    status_code=status.HTTP_200_OK
)
def get_usuario_id(usuario_id: Union[int, str], db: Session = Depends(get_db)):
    usuario = db.query(UsuarioModel).filter(
        UsuarioModel.id == usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    return usuario


@router.patch(
    "/{usuario_id}",
    response_model=UsuarioUpdateSchema,
    status_code=status.HTTP_200_OK,
)
def update_usuario(
    usuario_id: int,
    usuario: UsuarioUpdateSchema,
    db: Session = Depends(get_db)
):
    """
    Atualiza um usuário existente.
    - **usuario_id**: ID do usuário a ser atualizado
    - **usuario**: Dados para atualização (campos opcionais)
    """

    service = UsuarioService(db)
    usuario_atualizado = service.atualizar_usuario(usuario_id, usuario)
    if usuario_atualizado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    return usuario_atualizado


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario_delete = (
        db.query(UsuarioModel).filter(UsuarioModel.id == usuario_id).first()
    )
    if not usuario_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    db.delete(usuario_delete)
    db.commit()
    logging.info(f"Usuário deletado com sucesso: {usuario_delete.email}")
    return {"message": "Usuário deletado com sucesso"}


@router.get("/me/")
def get_me(current_user: Annotated[UsuarioSchema,
                                   Depends(get_current_active_user)]):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não autenticado"
        )

    return {
        "id": current_user.id,
        "nome": current_user.nome,
        "email": current_user.email,
    }
