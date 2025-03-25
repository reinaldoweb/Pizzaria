from fastapi import FastAPI
from app.core.database import engine, Base
from app.api.v1.api import api_router
import logging

app: FastAPI = FastAPI(title="Fast Pizzaria", version="0.1.0")

app.include_router(api_router)


# Configuração dos logs
logging.basicConfig(
    # Nível mínimo dos logs (INFO, DEBUG, WARNING, ERROR, CRITICAL)
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",  # Formato do log
    handlers=[
        logging.StreamHandler(),  # Exibe os logs no terminal
        logging.FileHandler("logs.txt"),  # Salva os logs no arquivo logs.txt
    ],
)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info", reload=True)
