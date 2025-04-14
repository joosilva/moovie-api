import json

from fastapi import APIRouter, Depends, Header

from src.api.response.moovies_exception_response import MooviesExceptionResponse
from src.api.response.router_response import RouterResponse
from src.api.response.enums.router_response_enum import RouterResponseEnum
from src.domain.dto.avaliacao_dto import AvaliacaoDTO
from src.domain.service.avaliacao_service import AvaliacaoService
from src.domain.service.dependencies.service_factory import get_avaliacao_service

router = APIRouter(prefix = "/avaliacao", tags = ["Avaliação"])


@router.post("/filme/{id_filme}", status_code = 201, responses = {
    201: {"model": RouterResponse, "description": "Título Avaliado com Sucesso"},
    400: {"model": MooviesExceptionResponse, "description":  "Token Vazio"},
    401: {"model": MooviesExceptionResponse, "description": "Token Expirado | Token Inválido"},
    422: {"model": MooviesExceptionResponse, "description": "Body Request Inválido | Titulo não Encontrado"},
    500: {"model": MooviesExceptionResponse, "description": "Internal Server Error"}
})
def avaliar_filme(id_filme: int, avaliacao: AvaliacaoDTO,
        access_token: str = Header(..., alias = "Authorization"),
        avaliacao_service: AvaliacaoService = Depends(get_avaliacao_service)):
    
    response = RouterResponse(RouterResponseEnum.TITULO_AVALIADO)
    return json.loads(response.model_dump_json())


@router.put("/filme/{id_filme}", status_code = 200, responses = {
    200: {"model": RouterResponse, "description": "Título Avaliado com Sucesso"},
    400: {"model": MooviesExceptionResponse, "description":  "Token Vazio"},
    401: {"model": MooviesExceptionResponse, "description": "Token Expirado | Token Inválido"},
    422: {"model": MooviesExceptionResponse, "description": "Body Request Inválido | Titulo não Encontrado"},
    500: {"model": MooviesExceptionResponse, "description": "Internal Server Error"}
})
def atualizar_avaliacao_filme(id_filme: int, avaliacao: AvaliacaoDTO,
        access_token: str = Header(..., alias = "Authorization")):
    
    response = RouterResponse(RouterResponseEnum.TITULO_AVALIADO)
    return json.loads(response.model_dump_json())


@router.post("/serie/{id_serie}", status_code = 201, responses = {
    201: {"model": RouterResponse, "description": "Título Avaliado com Sucesso"},
    400: {"model": MooviesExceptionResponse, "description":  "Token Vazio"},
    401: {"model": MooviesExceptionResponse, "description": "Token Expirado | Token Inválido"},
    422: {"model": MooviesExceptionResponse, "description": "Body Request Inválido | Titulo não Encontrado"},
    500: {"model": MooviesExceptionResponse, "description": "Internal Server Error"}
})
def avaliar_serie(id_serie: int, avaliacao: AvaliacaoDTO,
        access_token: str = Header(..., alias = "Authorization")):
    
    response = RouterResponse(RouterResponseEnum.TITULO_AVALIADO)
    return json.loads(response.model_dump_json())


@router.put("/serie/{id_serie}", status_code = 200, responses = {
    200: {"model": RouterResponse, "description": "Título Avaliado com Sucesso"},
    400: {"model": MooviesExceptionResponse, "description":  "Token Vazio"},
    401: {"model": MooviesExceptionResponse, "description": "Token Expirado | Token Inválido"},
    422: {"model": MooviesExceptionResponse, "description": "Body Request Inválido | Titulo não Encontrado"},
    500: {"model": MooviesExceptionResponse, "description": "Internal Server Error"}
})
def atualizar_avaliacao_serie(id_serie: int, avaliacao: AvaliacaoDTO,
        access_token: str = Header(..., alias = "Authorization")):
    
    response = RouterResponse(RouterResponseEnum.TITULO_AVALIADO)
    return json.loads(response.model_dump_json())
