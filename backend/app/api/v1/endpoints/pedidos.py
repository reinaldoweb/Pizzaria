from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.pedido_model import PedidoModel
from app.schemas.pedido import PedidoSchema

router = APIRouter()


@router.post(
    '/', status_code=status.HTTP_201_CREATED,
    response_model=PedidoSchema)
async def criar_pedido(
    cliente_id: int,
    produto_id: int,
    quantidade: int,
):
    db: Session = get_db()
    novo_pedido = PedidoModel(
        cliente_id=cliente_id, produto_id=produto_id, quantidade=quantidade)
    await db.add(novo_pedido)
    await db.commit()
    await db.refresh(novo_pedido)
    return novo_pedido


@router.get('/',
            response_model=List[PedidoSchema], status_code=status.HTTP_200_OK)
async def listar_pedidos(db: Session = Depends(get_db)):
    pedidos = db.query(PedidoModel).all()
    return pedidos


@router.get('/{pedido_id}', response_model=PedidoSchema,
            status_code=status.HTTP_202_ACCEPTED)
async def get_pedido_id(pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.query(PedidoModel).filter(
     PedidoModel.id == pedido_id).one_or_none()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido


@router.put('/{pedido_id}', response_model=PedidoSchema,
            status_code=status.HTTP_202_ACCEPTED)
async def atualizar_pedido_id(
    pedido_id: int,
    cliente_id: Optional[int] = None,
    produto_id: Optional[int] = None,
):
    db: Session = get_db()
    pedido = db.query(PedidoModel).filter(
        PedidoModel.id == pedido_id).one_or_none()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    await db.commit()
    await db.refresh(pedido)
    return pedido


@router.delete('/{pedido_id}', status_code=status.HTTP_204_NO_CONTENT)
async def deletar_pedido_id(pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.query(PedidoModel).filter(
        PedidoModel.id == pedido_id).one_or_none()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    db.delete(pedido)
    db.commit()
    return {"message": "Pedido deletado com sucesso"}
