from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.cliente_model import ClienteModel


router = APIRouter()


@router.post(
    "/clientes", status_code=status.HTTP_201_CREATED,
    response_model=ClienteModel
)
async def criar_cliente(
    nome: str, endereco: str, telefone: str, db: Session = Depends(get_db)
):
    novo_cliente = ClienteModel(nome=nome, endereco=endereco,
                                telefone=telefone)
    await db.add(novo_cliente)
    await db.commit()
    await db.refresh(novo_cliente)
    return novo_cliente


@router.get("/clientes", response_model=List[ClienteModel])
async def listar_clientes(db: Session = Depends(get_db)):
    clientes = db.query(ClienteModel).all()
    return clientes


@router.get(
    "/clientes/{cliente_id}",
    response_model=ClienteModel,
    status_code=status.HTTP_200_OK,
)
async def buscar_cliente_por_id(cliente_id: int,
                                db: Session = Depends(get_db)):
    cliente = db.query(ClienteModel).filter(
        ClienteModel.id == cliente_id).one_or_none()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente


@router.put(
    "/clientes/{cliente_id}",
    response_model=ClienteModel,
    status_code=status.HTTP_200_OK,
)
async def atualizar_cliente(
    cliente_id: int,
    nome: str,
    endereco: str,
    telefone: str,
    db: Session = Depends(get_db),
):
    cliente = db.query(ClienteModel).filter(
        ClienteModel.id == cliente_id).one_or_none()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    cliente.nome = nome
    cliente.endereco = endereco
    cliente.telefone = telefone
    await db.commit()
    await db.refresh(cliente)
    return cliente


@router.delete(
    "/clientes/{cliente_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=ClienteModel(),
)
async def deletar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(ClienteModel).filter(
        ClienteModel.id == cliente_id).one_or_none()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    db.delete(cliente)
    db.commit()
    return {"message": "Cliente deletado com sucesso"}
