import pytest
from datetime import datetime
from app.models.usuario_model import UsuarioModel
from app.core.security import gerar_hash_senha
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.main import app
from app.core.database import get_db

client = TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def limpar_banco():
    db: Session = next(get_db())

    # Limpa as tabelas de teste antes de cada teste
    tabelas = [
        "usuarios",
        "clientes",
        ]
    db.execute(text("SET session_replication_role = 'replica';"))

    for tabela in tabelas:
        db.execute(text(f"TRUNCATE TABLE {tabela} RESTART IDENTITY CASCADE"))

    db.execute(text("SET session_replication_role = 'origin';"))
    db.commit()
    yield


@pytest.fixture
def token_usuario_admin():
    """Fixture para criar um usuário admin e retornar o token de acesso."""
    db: Session = next(get_db())

    # Cria um usuário admin para os testes
    usuario = UsuarioModel(
        nome="usuario_admin",
        email="usuario_admin@email.com",
        senha_hash=gerar_hash_senha("senha_admin"),
        data_criacao=datetime.now(),
        is_admin=True,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    # Obtém o token de acesso para o usuário admin
    response = client.post(
        "/auth/token",
        data={"username": "usuario_admin@email.com", "password": "senha_admin"}
    )

    token = response.json()["access_token"]
    return token
