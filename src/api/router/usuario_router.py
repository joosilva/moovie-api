from fastapi import APIRouter, Depends, Header
from fastapi.security import HTTPBearer

from src.api.response.moovies_exception_response import MooviesExceptionResponse
from src.domain.dto.password_change_dto import PasswordChangeDTO
from src.domain.dto.usuario_dto import UsuarioDTO
from src.domain.dto.usuario_new_dto import UsuarioNewDTO
from src.domain.dto.usuario_update_dto import UsuarioUpdateDTO
from src.domain.service.usuario_service import UsuarioService
from src.domain.service.dependencies.service_factory import get_usuario_service

router = APIRouter(prefix = "/usuarios", tags = ["usuarios"])

security = HTTPBearer()

@router.post("", status_code = 201, responses = {
    400: {"model": MooviesExceptionResponse, "description": "Usuário já Existe | Token Vazio"},
    401: {"model": MooviesExceptionResponse, "description": "Token Expirado | Token Inválido"},
    422: {"model": MooviesExceptionResponse, "description": "Body Request Inválido"},
    500: {"model": MooviesExceptionResponse, "description": "Internal Server Error"}
})
def criar_usuario(usuario: UsuarioNewDTO, 
        usuario_service: UsuarioService = Depends(get_usuario_service)) -> UsuarioDTO:
    return usuario_service.cria_novo_usuario(usuario)


@router.put("", status_code = 200, responses = {
    400: {"model": MooviesExceptionResponse, "description": "Token Vazio"},
    401: {"model": MooviesExceptionResponse, "description": "Token Expirado | Token Inválido"},
    422: {"model": MooviesExceptionResponse, "description": "Body Request Inválido | Usuário Inválido | Usuário já Existe"},
    500: {"model": MooviesExceptionResponse, "description": "Internal Server Error"}
})
def atualizar_dados_usuario(dados_usuario: UsuarioUpdateDTO, 
        access_token: str = Header(..., alias = "Authorization"),
        usuario_service: UsuarioService = Depends(get_usuario_service)) -> UsuarioDTO:
    return usuario_service.atualiza_dados_usuario(dados_usuario, access_token)


@router.put("/password", status_code = 200, responses = {
    400: {"model": MooviesExceptionResponse, "description": "Token Vazio"},
    401: {"model": MooviesExceptionResponse, "description": "Token Expirado | Token Inválido"},
    422: {
            "model": MooviesExceptionResponse, 
            "description": "Body Request Inválido | Usuário Inválido | Usuário já Existe | Senha Divergente"
    },
    500: {"model": MooviesExceptionResponse, "description": "Internal Server Error"}
})
def atualizar_senha_usuario(senhas: PasswordChangeDTO, 
        access_token: str = Header(..., alias = "Authorization"),
        usuario_service: UsuarioService = Depends(get_usuario_service)):
    usuario_service.atualiza_senha_usuario(senhas, access_token)


@router.delete("", status_code = 204, responses = {
    400: {"model": MooviesExceptionResponse, "description": "Token Vazio"},
    401: {"model": MooviesExceptionResponse, "description": "Token Expirado | Token Inválido"},
    422: {"model": MooviesExceptionResponse, "description": "Body Request Inválido | Usuário Inválido"},
    500: {"model": MooviesExceptionResponse, "description": "Internal Server Error"}
})
def deletar_usuario(access_token: str = Header(..., alias = "Authorization"),
        usuario_service: UsuarioService = Depends(get_usuario_service)):
    usuario_service.exclui_usuario(access_token)
