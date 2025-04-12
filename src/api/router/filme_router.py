from fastapi import APIRouter, Header

from src.api.response.moovies_exception_response import MooviesExceptionResponse

router = APIRouter(prefix = "/filmes", tags = ["filmes"])

@router.get("", status_code = 200, responses = {
    400: {"model": MooviesExceptionResponse, "description":  "Token Vazio"},
    401: {"model": MooviesExceptionResponse, "description": "Token Expirado | Token Inválido"},
    422: {"model": MooviesExceptionResponse, "description": "Body Request Inválido"},
    500: {"model": MooviesExceptionResponse, "description": "Internal Server Error"}
})
def listar_filmes(access_token: str = Header(..., alias = "Authorization")):
    return
    

@router.get("/{id_usuario}/recomendacoes", status_code = 200, responses = {
    400: {"model": MooviesExceptionResponse, "description":  "Token Vazio"},
    401: {"model": MooviesExceptionResponse, "description": "Token Expirado | Token Inválido"},
    422: {"model": MooviesExceptionResponse, "description": "Body Request Inválido"},
    500: {"model": MooviesExceptionResponse, "description": "Internal Server Error"}
})
def listar_recomendacoes_usuario(id_usuario: int,
        access_token: str = Header(..., alias = "Authorization")):
    return
