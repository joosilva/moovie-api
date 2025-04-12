from fastapi import Depends
from sqlalchemy.orm import Session

from src.config.database import DatabaseConfig
from src.domain.service.auth_service import AuthService
from src.domain.service.token_service import TokenService
from src.domain.service.usuario_service import UsuarioService

db = DatabaseConfig()

def get_auth_service(db: Session = Depends(db.get_db)) -> AuthService:
    return AuthService(db)

def get_token_service(db: Session = Depends(db.get_db)) -> TokenService:
    return TokenService(db)

def get_usuario_service(db: Session = Depends(db.get_db)) -> UsuarioService:
    return UsuarioService(db)
