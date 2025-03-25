from typing import Optional
from sqlalchemy.orm import Session
from app.models.usuario_model import UsuarioModel
from app.schemas.usuario import UsuarioUpdateSchema
from app.core.security import gerar_hash_senha
import logging


logger = logging.getLogger(__name__)


class UsuarioUpdateService:
    def atualizar_usuario(
     self, db: Session, usuario_id: int, usuario_update: UsuarioUpdateSchema
     ) -> Optional[UsuarioModel]:

        # Atualiza um usuariio existente
        usuario = self.db.query(UsuarioModel).filter(
            UsuarioModel.id == usuario_id).first()

        if not usuario:
            return None

        # Atualiza os dados do usuário
        update_data = usuario_update.dict(exclude_unset=True)

        if "senha" in update_data:
            update_data["senha_hash"] = gerar_hash_senha(update_data["senha"])

        for field, value in update_data.items():
            setattr(usuario, field, value)

        try:
            # Salva as alterações no banco de dados
            db.commit()
            db.refresh(usuario)
            logger.info(f"Usuário atualizado com sucesso: {usuario.email}")
            return usuario
        except Exception as e:
            # Se houver algum erro, desfaz as alterações
            db.rollback()
            logger.error(f"Erro ao atualizar o usuário: {str(e)}")
            raise
