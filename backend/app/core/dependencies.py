from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from app.core.auth import verificar_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login_token")


def obter_usuario_logado(token: str = Security(oauth2_scheme)):
    try:
        payload = verificar_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
