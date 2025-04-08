from datetime import datetime
from fastapi.testclient import TestClient
from ..main import app
from app.models.usuario_model import UsuarioModel
from app.core.database import get_db
from app.core.security import gerar_hash_senha
from sqlalchemy.orm import Session

cliente = TestClient(app)


def test_criar_cliente_autenticado():
    db: Session = next(get_db())

    # Cria um usuário
    usuario = UsuarioModel(
        nome="João Teste2",
        email="joaoteste2@example.com",
        data_criacao=datetime.now(),
        is_admin=False,
        senha_hash=gerar_hash_senha("senha123"),
    )
    db.add(usuario)
    db.commit()
    # db.refresh(usuario)

    # Faz login para obeter o token de acesso
    login_data = {"username": "joaoteste2@example.com", "password": "senha123"}

    response = cliente.post("/auth/token", data=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Requisição para criar um cliente autenticado
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "nome": "Joao Teste2",
        "endereco": "Rua das Flores Verdes",
        "telefone": "123456789",
    }

    response = cliente.post("/clientes/", json=payload, headers=headers)
    assert response.status_code == 201
    assert response.json()["nome"] == "Joao Teste2"
