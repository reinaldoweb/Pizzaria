from datetime import datetime
from fastapi.testclient import TestClient
from backend.main import app
from app.models.usuario_model import UsuarioModel
from app.models.cliente_model import ClienteModel
from app.core.database import get_db
from app.core.security import gerar_hash_senha
from sqlalchemy.orm import Session

client = TestClient(app)


def test_atualizar_cliente_sucesso():
    db: Session = next(get_db())

    # Cria um usuário
    usuario = UsuarioModel(
        nome="Teste3",
        email="teste3@example.com",
        data_criacao=datetime.now(),
        is_admin=False,
        senha_hash=gerar_hash_senha("123456"),
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    # Cria um cliente associado ao usuário
    cliente = ClienteModel(
        nome="Fernando da Silva Sauro",
        endereco="Rua das Flores Verdes",
        telefone="123456789",
        usuario_id=usuario.id,
    )
    db.add(cliente)
    db.commit()
    db.refresh(cliente)

    # Faz login
    login_data = {"username": "teste3@example.com", "password": "123456"}
    response = client.post("/auth/token", data=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Faz o cabeçalho de autorização
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "nome": "Fernando da Silva Sauro",
        "endereco": "Rua das Flores Verdes",
        "telefone": "123456789",
    }

    # Faz a requisição PATCH para atualizar o cliente
    response = client.patch(
        f"/clientes/{cliente.id}", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["nome"] == "Fernando da Silva Sauro"
    assert response.json()["endereco"] == "Rua das Flores Verdes"
    assert response.json()["telefone"] == "123456789"

    db.close()
