from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.usuario_model import UsuarioModel
from app.schemas.usuario import (UsuarioSchema, UsuarioCreateSchema,
                                 UsuarioUpdateSchema)
from app.core.security import gerar_hash_senha


router = APIRouter()


@router.post("/", response_model=UsuarioSchema,
             status_code=status.HTTP_201_CREATED)
def create_usuario(usuario: UsuarioCreateSchema,
                   db: Session = Depends(get_db)):
    usuario_existente = db.query(UsuarioModel).filter(
        UsuarioModel.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="E-mail já cadastrado")

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

    if novo_usuario:
        raise HTTPException(status_code=status.HTTP_201_CREATED,
                            detail="Usuário criado com sucesso")
    return UsuarioSchema.model_validate(novo_usuario)


@router.get("/", response_model=List[UsuarioSchema],
            status_code=status.HTTP_200_OK)
def get_usuarios(db: Session = Depends(get_db)):
    return db.query(UsuarioModel).all()


@router.get(
    "/{usuario_id}", response_model=UsuarioSchema,
    status_code=status.HTTP_200_OK
)
def get_usuario_id(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioModel).filter(
        UsuarioModel.id == usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    return usuario


@router.put(
    "/{usuario_id}", response_model=UsuarioSchema,
    status_code=status.HTTP_202_ACCEPTED
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

    usuario_update.nome = usuario.nome
    usuario_update.email = usuario.email
    usuario_update.senha_hash = usuario.senha

    db.commit()
    db.refresh(usuario_update)
    if usuario_update:
        raise HTTPException(status_code=status.HTTP_202_ACCEPTED,
                            detail="Usuário atualizado com sucesso")
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
    return {"message": "Usuário deletado com sucesso"}
