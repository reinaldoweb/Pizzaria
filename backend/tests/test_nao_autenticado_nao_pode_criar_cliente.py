from fastapi.testclient import TestClient
from backend.main import app


client = TestClient(app)


def test_nao_autenticado_nao_pode_criar_cliente():

    payload = {
        "nome": "Novo Cliente",
        "telefone": "123456789",
        "endereco": "Rua Nova, 123",

    }
    # Faz a requisição se enviar tonken
    response = client.post("/clientes/", json=payload)
    assert response.status_code == 401
