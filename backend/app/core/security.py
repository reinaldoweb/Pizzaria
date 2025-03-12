from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verificar_senha(senha: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha, senha_hash)


def gerar_hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)
