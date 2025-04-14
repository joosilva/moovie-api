from fastapi import APIRouter, Depends, Header, Query

from typing import List, Optional

from src.api.response.moovies_exception_response import MooviesExceptionResponse
from src.domain.dto.filme_dto import FilmeDTO
from src.domain.service.dependencies.service_factory import get_filme_service
from src.domain.service.filme_service import FilmeService

router = APIRouter(prefix = "/filmes", tags = ["Filmes"])

@router.get("", status_code = 200, responses = {
    400: {"model": MooviesExceptionResponse, "description":  "Token Vazio"},
    401: {"model": MooviesExceptionResponse, "description": "Token Expirado | Token Inválido"},
    422: {"model": MooviesExceptionResponse, "description": "Body Request Inválido"},
    500: {"model": MooviesExceptionResponse, "description": "Internal Server Error"}
})
def listar_filmes(access_token: str = Header(..., alias = "Authorization"),
        filme_service: FilmeService = Depends(get_filme_service)) -> List[FilmeDTO]:
    
    return filme_service.busca_filmes_e_avaliacoes_usuario(access_token)
    

@router.get("/{id_usuario}/recomendacoes", status_code = 200, responses = {
    400: {"model": MooviesExceptionResponse, "description":  "Token Vazio"},
    401: {"model": MooviesExceptionResponse, "description": "Token Expirado | Token Inválido"},
    422: {"model": MooviesExceptionResponse, "description": "Body Request Inválido"},
    500: {"model": MooviesExceptionResponse, "description": "Internal Server Error"}
})
def listar_recomendacoes_usuario(id_usuario: int,
        qtd_recomendacoes: Optional[int] = Query(10, description = "Quantidade de recomendações."),
        access_token: str = Header(..., alias = "Authorization"),
        filme_service: FilmeService = Depends(get_filme_service)) -> List[FilmeDTO]:
    
    return filme_service.busca_filmes_recomendados_usuario(access_token, qtd_recomendacoes)
