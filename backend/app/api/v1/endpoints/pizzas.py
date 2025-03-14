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
    nova_pizza = PizzaModel(**pizza.model_dump())
    await db.add(nova_pizza)
    await db.commit()
    await db.refresh(nova_pizza)

    if nova_pizza:
        raise HTTPException(status_code=status.HTTP_201_CREATED,
                            detail="Pizza criada com sucesso")
    return nova_pizza


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
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pizza não encontrada!"
        )
    return pizza


@router.put("/{pizza_id}",
            status_code=status.HTTP_200_OK, response_model=PizzaSchema)
async def update_pizza(id: int, pizza: PizzaSchema,
                       db: Session = Depends(get_db)):
    update_pizza = db.query(PizzaSchema).filter(PizzaModel.id == id).first()
    if update_pizza is None:
        raise
    update_pizza.nome = pizza.nome
    update_pizza.preco = pizza.preco
    update_pizza.descricao = pizza.massa
    update_pizza.sabor = pizza.sabor
    await db.commit()
    await db.refresh(update_pizza)
    if update_pizza:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail="Pizza atualizada com sucesso!")
    return update_pizza


@router.delete("/{pizza_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pizza(id: int, db: Session = Depends(get_db)):
    pizza = db.query(PizzaModel).filter(PizzaModel.id == id).first()
    if pizza is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pizza não encontrada!"
        )
    await db.delete(pizza)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
