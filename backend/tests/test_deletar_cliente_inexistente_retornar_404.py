from fastapi.testclient import TestClient
from backend.main import app


client = TestClient(app)


def test_deletar_cliente_inexistente_retornar_404(token_usuario_admin):

    cliente_id_inexistente = 9999

    # Tenta deletar um cliente inexistente
    response = client.delete(
        f"/clientes/{cliente_id_inexistente}",
        headers={"Authorization": f"Bearer {token_usuario_admin}"},
    )
    print("Response JSON:", response.json())
    assert response.status_code == 404
    assert response.json() == {"detail": "Cliente não encontrado"}
