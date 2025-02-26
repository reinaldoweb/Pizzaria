from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL correta para conexão com PostgreSQL
DATABASE_URL = "postgresql+psycopg2://admin:admin123@localhost:5455/pizzaria"

# Criar engine
engine = create_engine(DATABASE_URL, echo=True)

# Criar sessão do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()


# Função para obter uma sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
