from typing import Union

from fastapi import Depends
from sqlalchemy.orm import Session

from src.config.database import DatabaseConfig

from src.domain.dto.password_change_dto import PasswordChangeDTO
from src.domain.dto.usuario_dto import UsuarioDTO
from src.domain.dto.usuario_new_dto import UsuarioNewDTO
from src.domain.dto.usuario_update_dto import UsuarioUpdateDTO
from src.domain.exceptions.exceptions import SenhaDivergenteException, UsuarioExistenteException, UsuarioInvalidoException
from src.domain.service.base.base_service import BaseService
from src.domain.service.token_service import TokenService
from src.domain.repository.usuario_repository import UsuarioRepository

db = DatabaseConfig()

class UsuarioService(BaseService):
    
    def __init__(self, db: Session):
        self.db = db
        self.token_service = TokenService(db)
        self.usuario_repository = UsuarioRepository(db)
        
        
    def count_usuarios(self) -> int:
        return self.usuario_repository.count_usuarios()
    
        
    def cria_novo_usuario(self, usuario: UsuarioNewDTO) -> UsuarioDTO:
        self.verifica_usuario_ja_existente(usuario)

        usuario.senha = self.crypto.criptografar(usuario.senha)

        new_usuario = self.usuario_repository.cria_novo_usuario(usuario.to_model())
        
        return new_usuario.to_dto()
    
    def recupera_id_usuario_by_token(self, token_code: str) -> int:
        return self.token_service.recupera_id_usuario_by_token(token_code)
    
    
    def verifica_usuario_ja_existente(self, usuario: Union[UsuarioDTO, UsuarioUpdateDTO]):
        is_usuario_existente = self.usuario_repository.verifica_usuario_ja_existente(usuario.username, usuario.email)
        
        if is_usuario_existente:
            raise UsuarioExistenteException()
    
    
    def busca_usuario_by_username(self, username: str):
        return self.usuario_repository.busca_usuario_by_username(username)
    
    
    def atualiza_dados_usuario(self, usuario: UsuarioUpdateDTO, token_code: str) -> UsuarioDTO:
        id_usuario = self.recupera_id_usuario_by_token(token_code)
        
        if not id_usuario:
            raise UsuarioInvalidoException()
        
        self.verifica_usuario_ja_existente(usuario)
        
        usuario_model = usuario.to_model(id_usuario)
        
        return self.usuario_repository.atualiza_dados_usuario(usuario_model).to_dto()
    
    def atualiza_senha_usuario(self, senhas: PasswordChangeDTO, token_code: str):
        id_usuario = self.recupera_id_usuario_by_token(token_code)
        
        usuario = self.usuario_repository.busca_usuario_by_id(id_usuario)
        
        if not usuario:
            raise UsuarioInvalidoException()
        
        if not self.crypto.equals(senhas.senha_atual, usuario.senha_hash):
            raise SenhaDivergenteException()
        
        nova_senha = self.crypto.criptografar(senhas.senha_nova)
        
        self.usuario_repository.atualiza_senha_usuario(id_usuario, nova_senha)
        
        self.token_service.inativa_token_by_id_usuario(id_usuario)
    
    
    def exclui_usuario(self, token_code: str):
        id_usuario = self.recupera_id_usuario_by_token(token_code)
        
        if not id_usuario:
            raise UsuarioInvalidoException()
        
        self.usuario_repository.exclui_usuario(id_usuario)
        
        self.token_service.inativa_token_by_id_usuario(id_usuario)
