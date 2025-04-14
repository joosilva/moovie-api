from sqlalchemy.orm import Session

from src.domain.dto.login_dto import LoginDTO
from src.domain.dto.token_dto import TokenDTO
from src.domain.exceptions.exceptions import LoginInvalidoException, LoginVazioException
from src.domain.model.usuario import Usuario
from src.domain.service.base.base_service import BaseService
from src.domain.service.token_service import TokenService
from src.domain.service.usuario_service import UsuarioService

class AuthService(BaseService):
    
    def __init__(self, db: Session):
        self.db = db
        self.token_service = TokenService(db)
        self.usuario_service = UsuarioService(db)
    
    def valida_dados_login(self, login: LoginDTO) -> Usuario:
        if not login:
            raise LoginVazioException()
        
        usuario: Usuario = self.usuario_service.busca_usuario_by_username(login.username)
        
        if not usuario or not self.crypto.equals(login.senha, usuario.senha_hash):
            raise LoginInvalidoException
        
        return usuario        
    
    
    def loga_usuario(self, login: LoginDTO, duracao_token: int) -> TokenDTO:
        
        usuario = self.valida_dados_login(login)
        
        return self.token_service.gera_token(usuario, duracao_token)
    
    
    def desloga_usuario(self, token_code: str):
        self.token_service.inativa_token(token_code)
