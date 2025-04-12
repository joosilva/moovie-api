import uuid
import hashlib

from datetime import datetime, timedelta

from fastapi import Depends
from sqlalchemy.orm import Session

from src.config.database import DatabaseConfig
from src.domain.dto.token_dto import TokenDTO
from src.domain.exceptions.exceptions import TokenExpiradoException, TokenInvalidoException, TokenVazioException
from src.domain.model.token import Token
from src.domain.model.usuario import Usuario
from src.domain.repository.token_repository import TokenRepository
from src.domain.service.base_service import BaseService

db = DatabaseConfig()

class TokenService(BaseService):
    
    def __init__(self, db: Session):
        self.db = db
        self.token_repository = TokenRepository(db)
        
        
    def trata_token_code(self, token_code: str):
        return token_code.removeprefix("Bearer ")
                
    
    def inativa_token_by_id_usuario(self, id_usuario: int):
        self.token_repository.inativa_token_by_id_usuario(id_usuario)
    
    
    def gera_token(self, usuario: Usuario, duracao_token: int) -> TokenDTO:
        token_code: str = str(uuid.uuid4()) + usuario.senha_hash
        
        token = Token()
        token.token = hashlib.sha256(token_code.encode('utf-8')).hexdigest()
        token.id_usuario = usuario.id_usuario
        
        now = datetime.now()
        
        token.data_expiracao = now + timedelta(minutes = duracao_token) if duracao_token <= 30 else now + timedelta(minutes = 30)
        
        self.inativa_token_by_id_usuario(usuario.id_usuario)
        
        self.token_repository.salva_token(token)
        
        return token.to_dto()
    
    
    def valida_token(self, token_code: str):
        if not token_code or not token_code.strip():
            raise TokenVazioException()
        
        if not token_code.startswith("Bearer "):
            raise TokenInvalidoException()
        
        token_code = self.trata_token_code(token_code)
        
        token = self.token_repository.recupera_token(token_code)
        if not token:
            raise TokenInvalidoException()
        
        if token.is_expirado():
            raise TokenExpiradoException()
        
    
    def inativa_token(self, token_code: str): 
        token_code = self.trata_token_code(token_code)
               
        self.token_repository.inativa_token(token_code)
        
    
    def recupera_id_usuario_by_token(self, token_code: str) -> int: 
        token_code = self.trata_token_code(token_code)
               
        return self.token_repository.recupera_id_usuario_by_token(token_code)
