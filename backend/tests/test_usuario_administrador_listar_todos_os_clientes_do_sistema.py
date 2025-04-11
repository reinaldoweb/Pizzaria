from fastapi.testclient import TestClient
from backend.main import app
from app.core.security import gerar_hash_senha
from app.core.database import get_db
from app.models.usuario_model import UsuarioModel
from app.models.cliente_model import ClienteModel
from sqlalchemy.orm import Session

client = TestClient(app)


def test_listar_todos_os_clientes_do_sistema():

    db: Session = next(get_db())

    senha_admin = "admin123"
    senha_comum = "usuario123"

    # Criar um usuário administrador
    usuario_admin = UsuarioModel(
        nome="Administrador",
        email="admin@example.com",
        senha_hash=gerar_hash_senha(senha_admin),
        is_admin=True,
    )
    db.add(usuario_admin)
    db.commit()
    db.refresh(usuario_admin)

    # Criar um usuário comum
    usuario_comum = UsuarioModel(
        nome="Usuário Comum",
        email="usuario@example.com",
        senha_hash=gerar_hash_senha(senha_comum),
        is_admin=False,
    )
    db.add(usuario_comum)
    db.commit()
    db.refresh(usuario_comum)

    # Cliente do admin
    cliente_admin = ClienteModel(
        nome="Cliente do Administrador",
        telefone="999999999",
        endereco="Rua do Admin, 123",
        usuario_id=usuario_admin.id,
    )
    db.add(cliente_admin)

    # Clientes do usuário comum
    clientes_comum = [
        ClienteModel(
            nome=f"Cliente {i}",
            telefone=f"99999-00{i}",
            endereco=f"Rua Cliente {i}, nº {i * 10}",
            usuario_id=usuario_comum.id,
        )
        for i in range(10)
    ]
    db.add_all(clientes_comum)
    db.commit()

    # === LOGIN ADMIN ===
    login_response_admin = client.post(
        "/auth/token",
        data={"username": "admin@example.com", "password": senha_admin},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert login_response_admin.status_code == 200
    access_token_admin = login_response_admin.json()["access_token"]

    headers_admin = {"Authorization": f"Bearer {access_token_admin}"}
    response_admin = client.get("/clientes", headers=headers_admin)
    assert response_admin.status_code == 200

    clientes_admin = response_admin.json()
    assert len(clientes_admin) == 1

    # === LOGIN USUÁRIO COMUM ===
    login_response_comum = client.post(
        "/auth/token",
        data={"username": "usuario@example.com", "password": senha_comum},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert login_response_comum.status_code == 200
    access_token_comum = login_response_comum.json()["access_token"]

    headers_comum = {"Authorization": f"Bearer {access_token_comum}"}
    response_comum = client.get("/clientes", headers=headers_comum)
    assert response_comum.status_code == 200

    clientes_do_comum = response_comum.json()
    assert all(cliente["nome"].startswith("Cliente")
               for cliente in clientes_do_comum)
    assert all(
        "telefone" in cliente and "endereco" in cliente
        for cliente in clientes_do_comum
    )
    assert not any(
        cliente["nome"] == "Cliente do Administrador"
        for cliente in clientes_do_comum
    )

    db.close()
