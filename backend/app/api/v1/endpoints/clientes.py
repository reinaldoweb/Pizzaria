from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.cliente_model import ClienteModel
from app.schemas.cliente import ClienteBaseSchema, ClienteSchema, ClienteCreateSchema
from app.core.database import get_db
from app.core.dependencies import get_current_user as get_usuario_logado


router = APIRouter()


@router.post(
    "/", status_code=status.HTTP_201_CREATED,
    response_model=ClienteSchema,
)


def criar_cliente(
    cliente: ClienteCreateSchema,
    db: Session = Depends(get_db),
    usuario_logado=Depends(get_usuario_logado)
) -> ClienteModel:
    """
    Cria um novo cliente associado ao usuário logado.

    Args:
        cliente: Dados do cliente a ser criado
        db: Sessão do banco de dados
        usuario_logado: Usuário autenticado

    Returns:
        ClienteModel: O cliente criado

    Raises:
        HTTPException: 400 em caso de erro na criação
    """
    try:
        novo_cliente = ClienteModel(
            usuario_id=usuario_logado.id,
            **cliente.model_dump()  # Usa model_dump para evitar atribuição manual
        )

        db.add(novo_cliente)
        db.commit()
        db.refresh(novo_cliente)

        return novo_cliente

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar cliente: {str(e)}"
        )


@router.get("/", response_model=List[ClienteBaseSchema],
            status_code=status.HTTP_200_OK)

def listar_clientes(db: Session = Depends(get_db)):
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


@router.patch(
    "/{cliente_id}",
    response_model=ClienteSchema,
    status_code=status.HTTP_200_OK,
)
def cliente_update(
    cliente_id: int,
    cliente_up: ClienteBaseSchema,
    db: Session = Depends(get_db),
)->ClienteBaseSchema:

    # Busca o cliente no banco de dados

    cliente_db = db.query(
    ClienteModel).filter(
    ClienteModel.id == cliente_id
    ).first()

    # Verifica se o cliente existe

    if not cliente_db:
        raise HTTPException(status_code=404,
        detail="Cliente não encontrado"
    )

    # Atualliza apenas os campos que foram fornecdidos no payload

    cliente_update = cliente_up.model_dump(exclude_unset = True)

    for field, value in cliente_update.items():
        setattr(cliente_db, field, value)

    try:
        db.commit()
        db.refresh(cliente_db)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Erro ao atualizar pedido: {str(e)}")

    return cliente_db



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
