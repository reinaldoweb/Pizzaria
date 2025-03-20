from typing import Annotated
from fastapi import HTTPException, Security, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session
from app.core.auth import verificar_token
from app.core.database import get_db
from app.models.usuario_model import UsuarioModel
import logging

from app.schemas.usuario import UsuarioSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_current_user(
    token: Annotated[str, Security(oauth2_scheme)],
    db: Session = Depends(get_db)
) -> UsuarioSchema:
    try:
        payload = verificar_token(token)
        if not isinstance(payload, dict):
            logging.warning("Falha ao verificar token: payload inválido")
            raise HTTPException(status_code=401, detail="Token inválido")

        email: str = payload.get("sub")
        if not email:
            logging.warning("Token inválido: sub não encontrado")
            raise HTTPException(status_code=401, detail="Token inválido")

        logging.info(
            f"Buscando usuário com e-mail: {email}"
        )  # Adicionado para depuração

        usuario = db.query(UsuarioModel).filter(
            UsuarioModel.email == email).first()
        if usuario is None:
            logging.warning(f"Usuário não encontrado para o e-mail: {email}")
            raise HTTPException(
                status_code=404,
                detail="Usuário não encontrado",
                headers={"WWW-Authenticate": "Bearer"},
            )

        logging.info(f"Usuário encontrado: {usuario.id} - {usuario.nome}")

        return UsuarioSchema.model_validate(usuario)

    except JWTError as e:
        logging.warning(f"Erro ao verificar o token: {str(e)}")
        raise HTTPException(status_code=401, detail="Token inválido")


def get_current_active_user(
    current_user: Annotated[UsuarioSchema, Depends(get_current_user)],
) -> UsuarioSchema:
    if not current_user:
        logging.warning("get_current_active_user: Nenhum usuário autenticado")
        raise HTTPException(status_code=401, detail="Usuário não autenticado")

    if not current_user:
        logging.warning(f"Usuário inativo: {current_user.email}")
        raise HTTPException(status_code=400, detail="Usuário inativo")

    logging.info(f"Usuário autenticado: {current_user.email}")
    return current_user
