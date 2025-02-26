from fastapi import APIRouter
from app.api.v1.endpoints import pedidos, clientes, pizzas, usuarios

api_router = APIRouter()

api_router.include_router(pedidos.router, prefix="/pedidos", tags=["Pedidos"])
api_router.include_router(clientes.router, prefix="/clientes",
                          tags=["clientes"])
api_router.include_router(pizzas.router, prefix="/pizzas", tags=["pizzas"])
api_router.include_router(usuarios.router, prefix="/usuarios",
                          tags=["usuarios"])
