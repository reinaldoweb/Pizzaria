from sqlalchemy.orm import Session
from app.models.cliente_model import ClienteModel



def criar_cliente_service(db: Session, cliente_data: dict, usuario_id: int) -> ClienteModel:
    try:
        novo_cliente = ClienteModel(usuario_id=usuario_id, **cliente_data)
        db.add(novo_cliente)
        db.commit()
        db.refresh(novo_cliente)
        return novo_cliente
    except:
        db.rollback()
        raise

