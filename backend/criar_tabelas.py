from sqlalchemy import create_engine
from app.core.database import DATABASE_URL, Base

# Cria a engine do banco de dados
engine = create_engine(DATABASE_URL)


def create_tables():
    # Importa os modelos para garantir que SQLAlchemy os reconheça
    from app.models import __all_models

    # Apenas garantindo que a importação seja utilizada
    _ = __all_models  # Ignora, mas mantém a importação sem erro
    print("Criando tabelas...")

    # Apaga todas as tabelas (Cuidado em produção!)
    Base.metadata.drop_all(bind=engine)  # Removido cascade="all"

    # Cria as tabelas
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso.")


if __name__ == "__main__":
    create_tables()
