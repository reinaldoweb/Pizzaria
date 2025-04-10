from typing import List
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
        Args:
            usuario_id: int
            cliente_data: dict
        Returns:
            ClienteModel: O cliente criado
            Exception: Caso ocorra algum erro durante a criação do cliente
        """
        cliente_existente = (
            self.db.query(ClienteModel)
            .filter(ClienteModel.usuario_id == usuario_id)
            .first()
        )
        if cliente_existente:
            raise ValueError("Cliente já cadastrado")
        try:
            novo_cliente = ClienteModel(**cliente_data, usuario_id=usuario_id)
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

    def listar_todos_clientes(
            self,
            usuario_id) -> List[ClienteModel]:
        """
        Lista todos os clientes do sistema
        :return: Lista de clientes do sistema
        """
        try:
            logger.info("Listando todos os clientes")
            clientes = self.db.query(ClienteModel).filter(
                ClienteModel.usuario_id == usuario_id
            ).all()
            logger.info(f"Encontrados {len(clientes)} clientes")
            return clientes
        except Exception as e:
            logger.exception(f"Erro ao listar clientes{str(e)}")
            raise

    def buscar_cliente_por_id(
            self,
            usuario_id: int
            ) -> ClienteModel:
        """
        Busca um cliente pelo seu ID.

        Args:
            cliente_id: ID do cliente a ser buscado

        Returns:
            ClienteModel: O cliente encontrado

        Raises:
            ValueError: Se o cliente não for encontrado
            Exception: Para erros inesperados no banco de dados
        """
        try:
            if not isinstance(usuario_id, int) or usuario_id <= 0:
                raise ValueError("ID do Cliente deve ser unúmero positivo")

            cliente_data = self.db.query(ClienteModel).filter(
                ClienteModel.usuario_id == usuario_id).first()

            if not cliente_data:
                logger.warning(f"Cliente não encontrado com ID {usuario_id}")
                raise ValueError(f"Cliente com ID {usuario_id} não encontrado")
            return cliente_data

        except ValueError as ve:
            logger.exception(f"Erro ao buscar cliente: {str(ve)}")
            raise
        except Exception as e:
            logger.exception(f"Erro ao buscar cliente: {str(e)}")
            raise Exception(f"Erro ao buscar cliente, {str(e)}")

    def atualizar_cliente(
        self,
        cliente_id: int,
        cliente_update: dict
    ) -> ClienteModel:

        """
        Atualiza um cliente existente no sistema.

        Args:
            cliente_id: ID do cliente a ser atualizado
            cliente_update: Dados atualizados do cliente

        Returns:
            ClienteModel: O cliente atualizado

        Raises:
            ValueError: Se o cliente não for encontrado
            Exception: Para erros inesperados no banco de dados
    """
        cliente = self.db.query(ClienteModel).filter_by(id=cliente_id).first()

        if not cliente:
            logger.warning(f"Cliente não encontrado com ID {cliente_id}")
            raise ValueError(f"Cliente com ID {cliente_id} não encontrado")

        if not cliente_update:
            logger.warning("Nenhum dado foi fornecido para atualizar o cliente"
                           ".")
            return cliente

        try:
            for field, value in cliente_update.items():
                setattr(cliente, field, value)

                self.db.commit()
                self.db.refresh(cliente)

                logger.info(f"Cliente atualizado: {cliente.nome}")
                return cliente

        except Exception:
            self.db.rollback()
            logger.exception("Erro ao atualizar cliente")
            raise Exception("Erro interno ao autlizar cliente")

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
