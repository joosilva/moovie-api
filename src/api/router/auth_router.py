from fastapi import APIRouter, Depends, Header, Query

from typing import Optional

from src.api.response.moovies_exception_response import MooviesExceptionResponse
from src.domain.dto.token_dto import TokenDTO
from src.domain.dto.login_dto import LoginDTO
from src.domain.service.auth_service import AuthService
from src.domain.service.dependencies.service_factory import get_auth_service

router = APIRouter()

@router.post("/login", status_code = 201, responses = {
    400: {"model": MooviesExceptionResponse, "description": "Login Vazio"},
    422: {"model": MooviesExceptionResponse, "description": "Body Request Inválido | Login Inválido"},
    500: {"model": MooviesExceptionResponse, "description": "Internal Server Error"}
})
def login(login: LoginDTO, duracao_token: Optional[int] = Query(30, description = "Duração do token em minutos."),
        auth_service: AuthService = Depends(get_auth_service)) -> TokenDTO:
    return auth_service.loga_usuario(login, duracao_token)


@router.post("/logout", status_code = 204, responses = {
    400: {"model": MooviesExceptionResponse, "description": "Token Vazio"},
    401: {"model": MooviesExceptionResponse, "description": "Token Expirado | Token Inválido"},
    422: {"model": MooviesExceptionResponse, "description": "Body Request Inválido"},
    500: {"model": MooviesExceptionResponse, "description": "Internal Server Error"}
})
def logout(access_token: str = Header(..., alias = "Authorization"),
        auth_service: AuthService = Depends(get_auth_service)):
    auth_service.desloga_usuario(access_token)
