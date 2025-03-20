from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.cliente_model import ClienteModel
from app.schemas.cliente import ClienteSchema
from app.core.database import get_db


router = APIRouter()


@router.post(
    "/", status_code=status.HTTP_201_CREATED,
    response_model=ClienteSchema,
)
async def criar_cliente(cliente: ClienteSchema, db: Session = Depends(get_db)):
    novo_cliente = ClienteModel(**cliente.model_dump())
    await db.add(novo_cliente)
    await db.commit()
    await db.refresh(novo_cliente)
    if novo_cliente:
        raise HTTPException(
            status_code=status.HTTP_201_CREATED,
            detail="Cliente criado com sucesso",
        )
    return novo_cliente


@router.get("/", response_model=List[ClienteSchema],
            status_code=status.HTTP_200_OK)
async def listar_clientes(db: Session = Depends(get_db)):
    clientes = db.query(ClienteModel).all()
    return clientes


@router.get(
    "/{cliente_id}",
    response_model=ClienteSchema,
    status_code=status.HTTP_200_OK,
)
async def buscar_cliente_por_id(cliente_id: int,
                                db: Session = Depends(get_db)):
    cliente_id = db.query(ClienteModel).filter(
        ClienteModel.id == cliente_id).one_or_none()
    if not cliente_id:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente_id


@router.put(
    "/{cliente_id}",
    response_model=ClienteSchema,
    status_code=status.HTTP_200_OK,
)
async def atualizar_cliente(
    cliente_id: int,
    nome: str,
    endereco: str,
    telefone: str,
    db: Session = Depends(get_db),
):
    cliente_up = db.query(ClienteModel).filter(
        ClienteModel.id == cliente_id).one_or_none()
    if not cliente_up:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    cliente_up.nome = nome
    cliente_up.endereco = endereco
    cliente_up.telefone = telefone
    await db.commit()
    await db.refresh(cliente_up)
    if cliente_up:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Cliente atualizado com sucesso",
        )
    return ClienteSchema.model_validate(cliente_up)


@router.delete(
    "/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente_del = db.query(ClienteModel).filter(
        ClienteModel.id == cliente_id).one_or_none()
    if not cliente_del:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    db.delete(cliente_del)
    db.commit()
    return {"message": "Cliente deletado com sucesso"}
