from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.pedido_model import PedidoModel
from app.schemas.pedido import PedidoSchema, PedidoCreateSchema
from app.models.cliente_model import ClienteModel
from app.models.pizza_model import PizzaModel
from app.core.dependencies import get_current_user as get_usuario_logado

router = APIRouter()


@router.post(
    '/', status_code=status.HTTP_201_CREATED,
    response_model=PedidoSchema)
def criar_pedido(pedido: PedidoCreateSchema,
                 db: Session = Depends(get_db),
                 usuario_logado=Depends(get_usuario_logado)):

    # Verificar se  o cliente existe
    cliente_id = pedido.usuario_logado.id
    cliente = db.query(ClienteModel).filter(
        ClienteModel.id == cliente_id).first()
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )

    # Verificar se a pizza existe
    pizza_id = pedido.pizza_id
    pizza = db.query(PizzaModel).filter(PizzaModel.id == pizza_id).first()
    if not pizza:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pizza não encontrada"
        )

    # Criar o pedido
    novo_pedido = PedidoModel(
        cliente_id=cliente_id,
        quantidade=pedido.quantidade,
        pizza_id=pedido.pizza_id,
        preco=pedido.preco * pedido.quantidade,
        status='pendente'  # status padrão para novo pedido

        )
    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)
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


@router.patch(
    '/{pedido_id}',
    response_model=PedidoSchema,
    status_code=status.HTTP_200_OK
)
def atualizar_pedido(
    pedido_id: int,
    pedido_update: PedidoSchema,
    db: Session = Depends(get_db)
) -> PedidoSchema:
    """
    Atualiza um pedido existente com os dados fornecidos.

    Args:
        pedido_id: ID do pedido a ser atualizado
        pedido_update: Dados parciais para atualização do pedido
        db: Sessão do banco de dados

    Returns:
        O pedido atualizado

    Raises:
        HTTPException: 404 se o pedido não for encontrado
    """
    # Busca o pedido no banco de dados
    pedido_db = db.query(PedidoModel).filter(PedidoModel.id == pedido_id).first()

    if not pedido_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado"
        )

    # Atualiza apenas os campos que foram fornecidos no payload
    update_data = pedido_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(pedido_db, field, value)

    try:
        db.commit()
        db.refresh(pedido_db)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar pedido: {str(e)}"
        )

    return pedido_db


@router.delete('/{pedido_id}', status_code=status.HTTP_204_NO_CONTENT)
async def deletar_pedido_id(pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.query(PedidoModel).filter(
        PedidoModel.id == pedido_id).one_or_none()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    db.delete(pedido)
    db.commit()
    return {"message": "Pedido deletado com sucesso"}
