from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.pizza_model import PizzaModel
from app.schemas.pizza import PizzaBaseSchema, PizzaCreateSchema, PizzaSchema


router = APIRouter()


@router.post("/",
             status_code=status.HTTP_201_CREATED,
             response_model=PizzaCreateSchema)
def create_pizza(
pizza: PizzaCreateSchema,
db: Session = Depends(get_db))-> PizzaModel:


    try:
        nova_pizza = PizzaModel(**pizza.model_dump())
        db.add(nova_pizza)
        db.commit()
        db.refresh(nova_pizza)

        return nova_pizza

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro ao tentar salvar a pizza: {e}"
)



@router.get("/", response_model=List[PizzaBaseSchema])
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


@router.patch('/{pizza_id}',
              response_model=PizzaSchema,
              status_code=status.HTTP_200_OK,
)
def update_pizza(
pizza_id: int,
pizza_update: PizzaBaseSchema,
db: Session = Depends(get_db
)
)-> PizzaSchema:


    # Busca a pizza no banco de dados
    pizza_db = db.query(PizzaModel).filter(PizzaModel.id == pizza_id).first()

    #Verifica se a pizza existe
    if pizza_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pizza nao encontrada!"
        )

    # Atualiza apenas os campos que foram fornecidos no payload
    update_pizza= pizza_update.model_dump(exclude_unset=True)

    for field, value in update_pizza.items():
        setattr(pizza_db, field, value)

    try:
        db.commit()
        db.refresh(pizza_db)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao atualizar a pizza")

    return pizza_db




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
