from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
import os
import logging

from app.core.security import verificar_senha
from app.core.database import get_db
from app.schemas.token import TokenSchema
from app.models.usuario_model import UsuarioModel

SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter()


@router.post("/token", response_model=TokenSchema)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    usuario = (
        db.query(UsuarioModel).filter(
            UsuarioModel.email == form_data.username).first()
    )
    if not usuario or not verificar_senha(form_data.password,
                                          usuario.senha_hash):
        logging.warning(
            f"Tentativa de login inválida para o email: {form_data.username}"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )
    token = criar_token({"sub": usuario.email})
    logging.info(f"Token criado para o email: {usuario.email}")
    return {"access_token": token, "token_type": "bearer"}


def criar_token(dados: dict,
                expiracao_minutos: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    a_expirar = datetime.utcnow().replace(tzinfo=timezone.utc) + timedelta(
        minutes=expiracao_minutos
    )
    dados.update({"exp": a_expirar})

    return jwt.encode(dados, SECRET_KEY, algorithm=ALGORITHM)


def verificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        logging.warning(f"Erro ao verificar o token: {e}")
        raise HTTPException(status_code=401, detail="Token inválido")
