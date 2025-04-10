from fastapi.testclient import TestClient
from backend.main import app
from app.models.usuario_model import UsuarioModel
from app.models.cliente_model import ClienteModel
from app.core.database import get_db
from app.core.security import gerar_hash_senha
from sqlalchemy.orm import Session

client = TestClient(app)


def test_usuario_autenticado_listar_apenas_clientes_que_pertecem_a_ele():
    db: Session = next(get_db())
    # Criar um usuário
    usuario_1 = UsuarioModel(
        nome="Teste",
        email="usuario1@example.com",
        senha_hash=gerar_hash_senha("senha123"),
    )
    db.add(usuario_1)
    db.commit()
    db.refresh(usuario_1)

    # Criar um cliente associado ao usuário 1
    cliente_1 = ClienteModel(
        nome="Cliente 1",
        telefone="123456789",
        endereco="Rua A, 123",
        usuario_id=usuario_1.id,
    )
    db.add(cliente_1)
    db.commit()
    db.refresh(cliente_1)

    # Criar um usuário 2
    usuario_2 = UsuarioModel(
        nome="Teste",
        email="usuario2@example.com",
        senha_hash=gerar_hash_senha("senha123"),
    )
    db.add(usuario_2)
    db.commit()
    db.refresh(usuario_2)

    # Criar um cliente associado ao usuário 2
    cliente_2 = ClienteModel(
        nome="Cliente 2",
        telefone="987654321",
        endereco="Rua B, 456",
        usuario_id=usuario_2.id,
    )
    db.add(cliente_2)
    db.commit()
    db.refresh(cliente_2)

    # Criar payload de login para o usuário 1
    login_data = {
        "username": "usuario1@example.com",
        "password": "senha123",
    }
    # Fazer login como o usuário 1
    response = client.post(
        "/auth/token",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Fazer uma solicitação GET para listar clientes com token de autenticação
    # do usuário 1
    response = client.get(
        "/clientes/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
