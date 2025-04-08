from app.models.usuario_model import UsuarioModel
from app.core.database import get_db
from app.core.security import gerar_hash_senha
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_deletar_cliente_id_inexistente():
    db: Session = next(get_db())

    usuario = UsuarioModel(
        nome='Inexistente',
        email='inexistente@example.com',
        senha_hash=gerar_hash_senha('123456'),
        data_criacao=datetime.now(),
        is_admin=True
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    # Login para obter o token de acesso
    login_data = {
        "username": "inexistente@example.com",
        "password": "123456"
    }
    response = client.post("/auth/token", data=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Enviar requisição DELETE com ID inexistente
    headers = {"Authorization": f"Bearer {token}"}
    response = client.delete("/clientes/99999", headers=headers)

    # validar resposta
    assert response.status_code == 404
    assert response.json() == {"detail": "Cliente não encontrado"}
