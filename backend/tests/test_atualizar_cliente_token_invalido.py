from fastapi.testclient import TestClient
from backend.main import app


client = TestClient(app)


def test_atualizar_cliente_token_invalido():
    headers = {"Authorization": "Bearer token_falso_invalid"}

    payload = {
        "nome": "João Silva",
        "endereco": "Nova Rua, 456",
        "telefone": "987654321"
    }

    response = client.patch("/clientes/3", headers=headers, json=payload)
    assert response.status_code == 401
    assert response.json() == {"detail": "Token inválido"}
