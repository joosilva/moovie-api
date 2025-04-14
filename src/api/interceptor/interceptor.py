from fastapi import FastAPI, Request

from src.config.database import DatabaseConfig
from src.domain.service.token_service import TokenService

ROTAS_PUBLICAS = [
    ("POST", "/login"),
    ("POST", "/usuario"),
    ("GET", "/docs"),
    ("GET", "/openapi.json")
]

db = DatabaseConfig()

def add_request_interceptor(app: FastAPI):
    
    @app.middleware("http")
    async def dispatch(request: Request, call_next):
        rota = (request.method, request.url.path)
        
        if rota in ROTAS_PUBLICAS:
            return await call_next(request)
        
        token_request: str = request.headers.get("Authorization")
        
        with db.session_scope() as db_session:
            token_service = TokenService(db_session)
            
            token_service.valida_token(token_request)
            
        return await call_next(request)
