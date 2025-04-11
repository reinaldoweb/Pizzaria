from app.core.security import gerar_hash_senha, verificar_senha


def test_gerar_hash_Senha():
    senha = "minha_senha_secreta"
    hash_senha = gerar_hash_senha(senha)

    # Vefifica se o retorno é uma string
    assert isinstance(hash_senha, str)
    # Verifica se o hash gerado não é igual à senha original
    assert hash_senha != senha


def test_verificar_senha():
    senha = "minha_senha_secreta"
    hash_senha = gerar_hash_senha(senha)

    # Verifica se a senha original é valida
    assert verificar_senha(senha, hash_senha) is True
    # Verifica se uma senha incorreta não é valida
    assert verificar_senha("senha_errada", hash_senha) is False
