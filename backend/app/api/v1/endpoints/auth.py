from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.usuario_model import UsuarioModel
from app.core.security import verificar_senha
from app.core.auth import criar_token
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Auth"])


class LoginSchema(BaseModel):
    email: str
    senha: str


@router.post("/login_token", status_code=status.HTTP_200_OK)
def login(dados: LoginSchema, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioModel).filter(
        UsuarioModel.email == dados.email).first()
    if not usuario or not verificar_senha(dados.senha, usuario.senha):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Usuário não encontrado")
    token = criar_token({"sub": usuario.email, "is_admin": usuario.is_admin})
    return {"access_token": token, "token_type": "bearer"}
