from datetime import datetime, timezone
from typing import Annotated, List, Union
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.usuario_model import UsuarioModel
from app.schemas.usuario import (UsuarioSchema,
                                 UsuarioCreateSchema, UsuarioUpdateSchema)
from app.core.security import gerar_hash_senha
from app.core.dependencies import get_current_active_user
import logging

router = APIRouter()


@router.post("/", response_model=UsuarioSchema,
             status_code=status.HTTP_201_CREATED)
def create_usuario(usuario: UsuarioCreateSchema,
                   db: Session = Depends(get_db)):
    usuario_existente = (
        db.query(UsuarioModel).filter(UsuarioModel.email == usuario.email)
        .first()
    )
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail já cadastrado"
        )

    senha_hash = gerar_hash_senha(usuario.senha)

    novo_usuario = UsuarioModel(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=senha_hash,
        data_criacao=datetime.now(timezone.utc),
        is_admin=usuario.is_admin,
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    logging.info(f"Usuário criado com sucesso: {novo_usuario.email}")
    return UsuarioSchema.model_validate(novo_usuario)


@router.get("/", response_model=List[UsuarioSchema],
            status_code=status.HTTP_200_OK)
def get_usuarios(db: Session = Depends(get_db)):
    return db.query(UsuarioModel).all()


@router.get(
    "/{usuario_id}", response_model=UsuarioSchema,
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
    status_code=status.HTTP_202_ACCEPTED,
)
def update_usuario(
    usuario_id: int, usuario: UsuarioUpdateSchema,
    db: Session = Depends(get_db)
):
    usuario_update = (
        db.query(UsuarioModel).filter(UsuarioModel.id == usuario_id).first()
    )
    if not usuario_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )

    if usuario_update.nome:
        usuario_update.nome = usuario.nome
    if usuario_update.email:
        usuario_update.email = usuario.email
    if usuario.senha:
        usuario_update.senha_hash = gerar_hash_senha(usuario.senha)

    db.commit()
    db.refresh(usuario_update)
    logging.info(f"Usuário atualizado com sucesso: {usuario_update.email}")
    return usuario_update


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
