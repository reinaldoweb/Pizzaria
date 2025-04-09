from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from backend.main import app
from app.models.usuario_model import UsuarioModel
from app.models.cliente_model import ClienteModel
from app.core.database import get_db
from app.core.security import gerar_hash_senha

client = TestClient(app)


def test_deletar_cliente_existente_com_sucesso():
    db: Session = next(get_db())

    # Cria um usuário de teste
    usuario = UsuarioModel(
        nome="Usuário de Teste",
        email="teste_delete1@example.com",
        senha_hash=gerar_hash_senha("senha123"),
        data_criacao=datetime.now(),
        is_admin=True
        )

    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    # Cria um cliente de teste relacionado ao usuário
    cliente = ClienteModel(
        nome="Cliente de Teste",
        endereco="Endereço de Teste",
        telefone="123456789",
        usuario_id=usuario.id,
        )
    db.add(cliente)
    db.commit()
    db.refresh(cliente)

    # Login para obter o token de autenticação
    login_data = {
        "username": "teste_delete1@example.com",
        "password": "senha123"
        }
    response = client.post("/auth/token", data=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Define o cabeçalho de autorização com o token JWT
    headers = {"Authorization": f"Bearer {token}"}
    response = client.delete(f"/clientes/{cliente.id}", headers=headers)
    print("Response JSON:", response.json())

    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 200
    assert response.json() == {"message": "Cliente deletado com sucesso"}
