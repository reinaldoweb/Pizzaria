from app.core.database import engine, Base


def create_tables():
    """
    Função para criar as tabelas no banco de dados.
    Esta função é chamada apenas uma vez, ao iniciar o banco.
    """

    # Importa os modelos
    from app.models import __all_models

    # Apenas garantindo que a importação seja utilizada
    _ = __all_models  # Ignora, mas mantém a importação sem erro

    print("Criando tabelas...")
    # Apaga todas as tabelas (Cuidado em produção!)
    Base.metadata.drop_all(bind=engine)
    # Cria as tabelas
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso.")


if __name__ == "__main__":
    create_tables()
