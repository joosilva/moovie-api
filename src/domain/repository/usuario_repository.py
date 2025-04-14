from datetime import datetime
from sqlalchemy import or_

from src.domain.model.usuario import Usuario
from src.domain.repository.base.base_repository import BaseRepository

class UsuarioRepository(BaseRepository):
    
    def count_usuarios(self) -> int:
        return self.db.query(Usuario).count()
    
    
    def verifica_usuario_ja_existente(self, username: str, email: str) -> bool:
        usuario = self.db.query(Usuario).filter(
            or_(
                Usuario.username == username,
                Usuario.email == email
            ),
            Usuario.data_exclusao.is_(None)
        ).first()
        
        return usuario is not None
    
    
    def cria_novo_usuario(self, usuario: Usuario) -> Usuario:
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        
        return usuario
    
    
    def busca_usuario_by_id(self, id_usuario: int) -> Usuario:
        usuario = self.db.query(Usuario).filter(
            Usuario.id_usuario == id_usuario
        ).first()
        
        return usuario

    
    def busca_usuario_by_username(self, username: str) -> Usuario:
        usuario = self.db.query(Usuario).filter(
            Usuario.username == username,
            Usuario.data_exclusao.is_(None)
        ).first()
        
        return usuario
    
    
    def atualiza_dados_usuario(self, usuario: Usuario) -> Usuario:
        usuario_existente = self.busca_usuario_by_id(usuario.id_usuario)
        
        if usuario_existente:
            if usuario.username:
                usuario_existente.username = usuario.username
            if usuario.nome:
                usuario_existente.nome = usuario.nome
            if usuario.email:
                usuario_existente.email = usuario.email
                
            self.db.commit()
            
        return usuario_existente
    
    
    def atualiza_senha_usuario(self, id_usuario: int, nova_senha: str):
        usuario = self.busca_usuario_by_id(id_usuario)
        
        if usuario:
            usuario.senha_hash = nova_senha
            
            self.db.commit()
      
    
    def exclui_usuario(self, id_usuario: int):
        usuario = self.busca_usuario_by_id(id_usuario)
        
        if usuario:
            usuario.data_exclusao = datetime.now()
            
            self.db.commit()
