from fastapi import Depends
from sqlalchemy.orm import Session

from src.config.database import DatabaseConfig
from src.domain.service.auth_service import AuthService
from src.domain.service.avaliacao_service import AvaliacaoService
from src.domain.service.filme_service import FilmeService
from src.domain.service.serie_service import SerieService
from src.domain.service.token_service import TokenService
from src.domain.service.usuario_service import UsuarioService

db = DatabaseConfig()

def get_auth_service(db: Session = Depends(db.get_db)) -> AuthService:
    return AuthService(db)

def get_avaliacao_service(db: Session = Depends(db.get_db)) -> AvaliacaoService:
    return AvaliacaoService(db)

def get_filme_service(db: Session = Depends(db.get_db)) -> FilmeService:
    return FilmeService(db)

def get_serie_service(db: Session = Depends(db.get_db)) -> SerieService:
    return SerieService(db)

def get_token_service(db: Session = Depends(db.get_db)) -> TokenService:
    return TokenService(db)

def get_usuario_service(db: Session = Depends(db.get_db)) -> UsuarioService:
    return UsuarioService(db)
