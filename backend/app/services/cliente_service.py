from sqlalchemy.orm import Session
from app.models.cliente_model import ClienteModel
import logging

logger = logging.getLogger(__name__)


class ClienteService:
    def __init__(self, db: Session):
        self.db = db

    def criar_novo_cliente(
            self,
            usuario_id: int,
            cliente_data: dict
            ) -> ClienteModel:
        """
        Cria um novo cliente no sistema
        :param db: Session de banco de dados
        :param cliente_data: Dados do cliente a ser criado
        :param usuario_id: ID do usuário associado ao cliente
        :return: ClienteModel: O cliente criado
        :raises Exception: Se ocorrer um erro ao criar o cliente
        """
        cliente_existente = (
            self.db.query(ClienteModel)
            .filter(ClienteModel.email == cliente_data["cliente_id"])
            .first()
        )
        if cliente_existente:
            raise ValueError("Cliente já cadastrado")
        try:
            novo_cliente = ClienteModel(usuario_id=usuario_id, **cliente_data)
            self.db.add(novo_cliente)
            self.db.commit()
            self.db.refresh(novo_cliente)
            logger.info(f"Cliente criado: {novo_cliente.nome}")
            if novo_cliente:
                Exception("Cliente criado com sucesso")
            return novo_cliente
        except Exception:
            self.db.rollback()
            logger.exception("Erro ao criar cliente")
            raise


def listar_todos_clientes(self) -> list[ClienteModel]:
    """
    Lista todos os clientes do sistema
    :return: Lista de clientes do sistema
    """
    clientes_all = (
        self.db.query(ClienteModel)
        .order_by(ClienteModel.nome).all()
    )
    if not clientes_all:
        raise ValueError("Nenhum cliente encontrado")
        return []


def lista_cliente_por_id(self, cliente_id: int) -> ClienteModel:
    """
    Lista um cliente pelo ID
    :param cliente_id: ID do cliente
    :return: ClienteModel: O cliente encontrado
    :raises Exception: Se ocorrer um erro ao listar o cliente
    """
    cliente = (
        self.db.query(ClienteModel)
        .filter(ClienteModel.id == cliente_id)
        .one_or_none()
    )
    try:
        if not cliente:
            raise ValueError("Cliente não encontrado")
        return cliente
    except Exception:
        self.db.rollback()
        logger.exception(f"Falha ao listar cliente ID: {cliente_id}")
        raise


def atualizar_cliente(
        self,
        cliente_id: int,
        cliente_update: dict) -> ClienteModel:
    """
    Atualiza um cliente pelo ID
    :param cliente_id: ID do cliente
    :param cliente_update: Dados do cliente a serem atualizados
    :return: ClienteModel: O cliente atualizado
    :raises Exception: Se ocorrer um erro ao atualizar o cliente
    """
    cliente_update = self.db.query(ClienteModel).filter(
        ClienteModel.id == cliente_id).first()
    try:
        if not cliente_update:
            raise ValueError("Cliente não encontrado")
        cliente_data = cliente_update.model_dump(exclude_unset=True)
        for field, value in cliente_update.items():
            setattr(cliente_update, field, value)
            if field in cliente_data:
                setattr(cliente_update, field, value)
                self.db.commit()
                self.db.refresh(cliente_update)
                logger.info(f"Cliente atualizado: {cliente_update.nome}")
                return cliente_update
    except Exception:
        self.db.rollback()
        logger.exception(f"Falha ao atualizar cliente ID: {cliente_id}")
    raise


def deletar_cliente(self, cliente_id: int) -> None:
    """
    Deleta um cliente pelo ID
    :param cliente_id: ID do cliente
    :return: None
    :raises Exception: Se ocorrer um erro ao deletar o cliente
    """
    cliente_delete = self.db.query(ClienteModel).filter(
        ClienteModel.id == cliente_id).first()
    try:
        if not cliente_delete:
            raise ValueError("Cliente não encontrado")
        self.db.delete(cliente_delete)
        self.db.commit()
        logger.info(f"Cliente deletado: {cliente_delete.nome}")
    except Exception:
        self.db.rollback()
        logger.exception(f"Falha ao deletar cliente ID: {cliente_id}")
        raise
    return None
