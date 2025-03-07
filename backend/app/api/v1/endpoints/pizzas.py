from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.pizza_model import PizzaModel
from app.schemas.pizza import PizzaSchema


router = APIRouter()


@router.post("/",
             status_code=status.HTTP_201_CREATED, response_model=PizzaSchema)
async def create_pizza(pizza: PizzaSchema, db: Session = Depends(get_db)):
    await db.add(pizza)
    await db.commit()
    await db.refresh(pizza)
    return pizza


@router.get("/", response_model=List[PizzaSchema])
async def read_pizzas(db: Session = Depends(get_db)):
    pizzas = db.query(PizzaModel).all()
    return pizzas


@router.get("/{pizza_id}",
            status_code=status.HTTP_200_OK, response_model=PizzaSchema)
async def read_pizza(id: int, db: Session = Depends(get_db)):
    pizza = db.query(PizzaModel).filter(PizzaModel.id == id).first()
    if pizza is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pizza not found"
        )
    return pizza


@router.put("/{pizza_id}",
            status_code=status.HTTP_200_OK, response_model=PizzaSchema)
async def update_pizza(id: int, pizza: PizzaSchema,
                       db: Session = Depends(get_db)):
    db_pizza = db.query(PizzaSchema).filter(PizzaModel.id == id).first()
    if db_pizza is None:
        raise
    db_pizza.nome = pizza.nome
    db_pizza.preco = pizza.preco
    db_pizza.descricao = pizza.massa
    db_pizza.sabor = pizza.sabor
    await db.commit()
    await db.refresh(db_pizza)
    return db_pizza


@router.delete("/{pizza_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pizza(id: int, db: Session = Depends(get_db)):
    pizza = db.query(PizzaModel).filter(PizzaModel.id == id).first()
    if pizza is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pizza not found"
        )
    await db.delete(pizza)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
