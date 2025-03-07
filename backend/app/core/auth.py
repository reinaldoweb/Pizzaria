from datetime import datetime, timedelta
from jose import JWTError, jwt


SECRETE_KEY = "fgsdgsfdg54354b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def criar_token(dados: dict,
                expiracao_minutos: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    a_expirar = datetime.now() + timedelta(minutes=expiracao_minutos)
    dados.update({"exp": a_expirar})
    return jwt.encode(dados, SECRETE_KEY, algorithm=ALGORITHM)


def verificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRETE_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
