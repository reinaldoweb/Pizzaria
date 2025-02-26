from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.pizza_model import PizzaModel


router = APIRouter()


@router.post("/pizzas/",
             status_code=status.HTTP_201_CREATED, response_model=PizzaModel)
async def create_pizza(pizza: PizzaModel, db: Session = Depends(get_db)):
    await db.add(pizza)
    await db.commit()
    await db.refresh(pizza)
    return pizza


@router.get("/pizzas/", response_model=List[PizzaModel])
async def read_pizzas(db: Session = Depends(get_db)):
    pizzas = db.query(PizzaModel).all()
    return pizzas


@router.get("/pizzas/{pizza_id}",
            status_code=status.HTTP_200_OK, response_model=PizzaModel)
async def read_pizza(id: int, db: Session = Depends(get_db)):
    pizza = db.query(PizzaModel).filter(PizzaModel.id == id).first()
    if pizza is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pizza not found"
        )
    return pizza


@router.put("/pizzas/{pizza_id}",
            status_code=status.HTTP_200_OK, response_model=PizzaModel)
async def update_pizza(id: int, pizza: PizzaModel,
                       db: Session = Depends(get_db)):
    db_pizza = db.query(PizzaModel).filter(PizzaModel.id == id).first()
    if db_pizza is None:
        raise
    db_pizza.nome = pizza.nome
    db_pizza.preco = pizza.preco
    db_pizza.descricao = pizza.massa
    db_pizza.sabor = pizza.sabor
    await db.commit()
    await db.refresh(db_pizza)
    return db_pizza


@router.delete("/pizzas/{pizza_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pizza(id: int, db: Session = Depends(get_db)):
    pizza = db.query(PizzaModel).filter(PizzaModel.id == id).first()
    if pizza is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pizza not found"
        )
    await db.delete(pizza)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
