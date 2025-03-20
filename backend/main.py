from fastapi import FastAPI
from app.core.database import engine, Base
from app.api.v1.api import api_router

app: FastAPI = FastAPI()

app.include_router(api_router)


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info", reload=True)
