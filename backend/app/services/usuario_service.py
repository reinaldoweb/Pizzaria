from typing import Optional
from sqlalchemy.orm import Session
from app.models.usuario_model import UsuarioModel
from app.schemas.usuario import UsuarioUpdateSchema
from app.core.security import gerar_hash_senha
import logging

logger = logging.getLogger(__name__)


class UsuarioService:
    def __init__(self, db: Session):
        self.db = db

    def criar_usuario(self, usuario_data: dict) -> UsuarioModel:
        """Cria um novo usuário no sistema"""
        usuario_existente = (
            self.db.query(UsuarioModel)
            .filter(UsuarioModel.email == usuario_data["email"])
            .first()
        )

        if usuario_existente:
            raise ValueError("E-mail já cadastrado")

        try:
            novo_usuario = UsuarioModel(**usuario_data)
            self.db.add(novo_usuario)
            self.db.commit()
            self.db.refresh(novo_usuario)
            logger.info(f"Usuário criado: {novo_usuario.email}")
            return novo_usuario
        except Exception:
            self.db.rollback()
            logger.exception("Erro ao criar usuário")
            raise

    def atualizar_usuario(
        self, usuario_id: int, usuario_update: UsuarioUpdateSchema
    ) -> Optional[UsuarioModel]:
        """Atualiza os dados de um usuário existente"""
        usuario_up = self.db.query(UsuarioModel).filter_by(
            id=usuario_id).first()

        if not usuario_up:
            return None

        update_data = usuario_update.model_dump(exclude_unset=True)

        if "senha" in update_data:
            update_data["senha_hash"] = gerar_hash_senha(
                update_data.pop("senha"))

        try:
            for field, value in update_data.items():
                setattr(usuario_up, field, value)

            self.db.commit()
            self.db.refresh(usuario_up)
            logger.info(f"Usuário atualizado: {usuario_up.email}")
            return usuario_up
        except Exception:
            self.db.rollback()
            logger.exception(f"Falha ao atualizar usuário ID: {usuario_id}")
            raise
