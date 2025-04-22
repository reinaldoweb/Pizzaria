from fastapi.testclient import TestClient
from backend.main import app  # ajuste o caminho se necessário


client = TestClient(app)


def test_criar_cliente_sem_autenticacao():
    payload = {
        "nome": "Cliente Teste",
        "endereco": "Rua Teste, 123",
        "telefone": "123456789",
        "usuario_id": 1,  # ID do usuário que está criando o cliente
    }
    response = client.post("/clientes/", json=payload)
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}
