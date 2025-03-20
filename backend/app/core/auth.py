from datetime import datetime, timedelta
from fastapi import HTTPException
from jose import JWTError, jwt
import os
import logging

SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def criar_token(dados: dict,
                expiracao_minutos: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    a_expirar = datetime.utcnow() + timedelta(minutes=expiracao_minutos)
    dados.update({"exp": a_expirar})
    return jwt.encode(dados, SECRET_KEY, algorithm=ALGORITHM)


def verificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        logging.warning(f"Erro ao verificar o token: {e}")
        raise HTTPException(status_code=401, detail="Token inválido")
