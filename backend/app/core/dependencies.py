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
        if not payload or not isinstance(payload, dict):
            logging.warning("Falha ao verificar token: payload inválido")
            raise HTTPException(status_code=401, detail="Token inválido")

        email: str = payload.get("sub")

        if not email:
            logging.warning("Token inválido: sub não encontrado")
            raise HTTPException(status_code=401, detail="Token inválido")

        logging.info(f"Buscando usuário com e-mail: {email}")

        usuario = db.query(UsuarioModel).filter(
            UsuarioModel.email == email).first()

        if usuario is None:
            logging.warning(f"Usuário não encontrado para o e-mail: {email}")
            raise HTTPException(
                status_code=404,
                detail="Usuário não encontrado",
                headers={"WWW-Authenticate": "Bearer"},
            )

        logging.info(f"Usuário autenticado: ID={usuario.id}")

        # Certifique-se de que UsuarioSchema é compatível com model_validate()
        return UsuarioSchema.model_validate(usuario)

    except JWTError as e:
        logging.error(f"Erro ao processar o token JWT: {e}")
        raise HTTPException(status_code=401, detail="Token inválido")
    except Exception as e:
        logging.error(f"Erro inesperado na autenticação: {e}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor")


def get_current_active_user(
    current_user: Annotated[UsuarioSchema, Depends(get_current_user)],
) -> UsuarioSchema:
    if not current_user:
        logging.warning("Nenhum usuário autenticado")
        raise HTTPException(status_code=401, detail="Usuário não autenticado")

    logging.info(f"Usuário autenticado: {current_user.email}")
    return current_user
