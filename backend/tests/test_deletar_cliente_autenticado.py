from datetime import datetime
from fastapi.testclient import TestClient
from backend.main import app
from app.models.usuario_model import UsuarioModel
from app.models.cliente_model import ClienteModel
from app.core.database import get_db
from app.core.security import gerar_hash_senha
from sqlalchemy.orm import Session


client = TestClient(app)


def test_deletar_cliente_autenticado():
    db: Session = next(get_db())

    # Criar um usuário para realizar a deleção
    usuario = UsuarioModel(
        nome="Usuario deleção",
        email="deletarcliente@exemplo.com",
        senha_hash=gerar_hash_senha("123456"),
        data_criacao=datetime.now(),
        is_admin=False
    )

    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    # Criar um cliente associado ao usuário
    cliente = ClienteModel(
        nome="Teste deleção",
        telefone="123456789",
        endereco="Rua deleção",
        usuario_id=usuario.id
    )
    db.add(cliente)
    db.commit()
    db.refresh(cliente)

    # Fazer o login do usuário
    login_data = {
        "username": "deletarcliente@exemplo.com",
        "password": "123456"
    }
    login_response = client.post("/auth/token", data=login_data)
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]

    # Envia a requisição para Deletar o cliente
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.delete(f"/clientes/{cliente.id}", headers=headers)
    assert response.status_code == 204
