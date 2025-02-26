from datetime import date
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.usuario_model import UsuarioModel

router = APIRouter()


@router.post("/usuarios/", response_model=UsuarioModel,
             status_code=status.HTTP_201_CREATED)
async def create_usuario(usuario: UsuarioModel, db: Session = Depends(get_db)):
    novo_usuario = UsuarioModel(nome=usuario.nome, email=usuario.email,
                                senha=usuario.senha_hash, data_criacao=date())
    await db.add(novo_usuario)
    await db.commit()
    await db.refresh(novo_usuario)
    return novo_usuario


@router.get("/usuarios/", response_model=List[UsuarioModel],
            status_code=status.HTTP_200_OK)
async def get_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(UsuarioModel).all()
    return usuarios


@router.get("/usuarios/{usuario_id}", response_model=UsuarioModel,
            status_code=status.HTTP_200_OK)
async def get_usuarios_id(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioModel).filter(
        UsuarioModel.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Usuário não encontrado")
    return usuario


@router.put("/usuarios/{usuario_id}", response_model=UsuarioModel,
            status_code=status.HTTP_202_ACCEPTED)
async def update_usuario(usuario_id: int, usuario: UsuarioModel,
                         db: Session = Depends(get_db)):
    usuario_update = db.query(UsuarioModel).filter(
        UsuarioModel.id == usuario_id).first()
    if not usuario_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Usuário não encontrado")
    usuario_update.nome = usuario.nome
    usuario_update.email = usuario.email
    usuario_update.senha_hash = usuario.senha_hash
    await db.commit()
    await db.refresh(usuario_update)
    return usuario_update


@router.delete("/usuarios/{usuario_id}",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario_delete = db.query(UsuarioModel).filter(
        UsuarioModel.id == usuario_id).first()
    if not usuario_delete:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    db.delete(usuario_delete)
    await db.commit()
    return {"message": "Usuário deletado com sucesso"}
