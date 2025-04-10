from datetime import datetime
from fastapi.testclient import TestClient
from backend.main import app
from app.models.usuario_model import UsuarioModel
from app.models.cliente_model import ClienteModel
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.core.security import gerar_hash_senha

client = TestClient(app)


def test_usuario_nao_pode_atualizar_cliente_de_outro():
    # Obtém a sessão do banco de dados
    db: Session = next(get_db())

    # Cria um usuário para testar
    usuario1 = UsuarioModel(
        nome="Usuario 1",
        email="usuario1@example.com",
        senha_hash=gerar_hash_senha("teste123"),
        data_criacao=datetime.now(),
        is_admin=True

    )
    db.add(usuario1)
    db.commit()
    db.refresh(usuario1)

    # Cria um cliente para testar
    cliente = ClienteModel(
        nome="Cliente Teste",
        endereco="Rua Teste, 123",
        telefone="1234567890",
        usuario_id=usuario1.id,
    )
    db.add(cliente)
    db.commit()
    db.refresh(cliente)

    # Cria usuário 2
    usuario2 = UsuarioModel(
        nome="Usuario 2",
        email="usuario2@example.com",
        senha_hash=gerar_hash_senha("teste123"),
        data_criacao=datetime.now(),
        is_admin=False
    )
    db.add(usuario2)
    db.commit()
    db.refresh(usuario2)

    # Login com usuario 2
    login_data = {
        "username": "usuario2@example.com",
        "password": "teste123"
    }
    response = client.post(
        "auth/token",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
                        )
    assert response.status_code == 200, response.text
    token = response.json().get("access_token")

    # Tentativa de atualizar cliente do outro usuario
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "nome": "Novo Nome",
        "endereco": "Nova Rua, 456",
        "telefone": "9876543210"
    }
    response = client.patch(
        f"/clientes/{cliente.id}", json=payload, headers=headers)

    # Veerifica que o acesso foi negado
    assert response.status_code == 403
    assert response.json() == {
        "detail": "Você não tem permissão para acessar este recurso."
        }
