"""
Testes unitários para o módulo de criação de usuários.
Objetivo do teste de Criação de Usuário?
Garantir que:
1. Um novo usuário pode ser criado com sucesso.
2. O sistema retorne os dados eperado(Id, nome, email, etc)
3. Não permita duplicidade de usuários com o mesmo email.

"""

from datetime import datetime
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_criar_usuario():
    # Verifica se já existe um usuário com o mesmo email
    # Dados de teste
    usuario_data = {
        "nome": "João da Silva",
        "email": "josea@example.com",
        "senha": "senha1234",
        "data_criacao": datetime.now().isoformat(),
        "is_admin": False
    }

    # Fazer a solicitação POST para a rota de criação de usuário
    response = client.post("/usuarios/", json=usuario_data)
    print(response.status_code)
    print(response.json())

    # Verificar se a resposta é bem-sucedida (código 201)
    assert response.status_code == 201
    data = response.json()

    # Verificar se os dados retornados correspondem aos dados enviados
    assert data["email"] == usuario_data["email"]
    assert "id" in data  # Verificar se o ID foi gerado
