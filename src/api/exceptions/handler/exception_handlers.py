from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

import json

from src.api.exceptions.moovies_exception import MooviesException
from src.api.response.moovies_exception_response import MooviesExceptionResponse
from src.domain.exceptions.enums.moovies_exception_enum import MooviesExceptionEnum


def exceptions_subclasses(cls):
    subclasses = set()
    for subclass in cls.__subclasses__():
        subclasses.add(subclass)
        subclasses.update(exceptions_subclasses(subclass))
    return subclasses

def gera_json_exception_generica(moovies_exception: MooviesException, exception: Exception) -> JSONResponse:
    exception_personalizada = MooviesExceptionResponse(
        exception = moovies_exception.error.nome,
        mensagem = f"{moovies_exception.error.mensagem} -> {str(exception)}"
    )
    
    return JSONResponse(
        status_code = moovies_exception.error.status_code,
        content = json.loads(exception_personalizada.model_dump_json())
    )

def exception_handlers(app: FastAPI):
    
    @app.exception_handler(Exception)
    async def exception_handler(request: Request, exception: Exception):
        if isinstance(exception, MooviesException):
            return JSONResponse(
                status_code=exception.error.status_code,
                content=json.loads(str(exception))
            )

        moovies_exception = MooviesException(MooviesExceptionEnum.INTERNAL_SERVER_ERROR)

        return gera_json_exception_generica(moovies_exception, exception)
    

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exception: RequestValidationError):
        moovies_exception = MooviesException(MooviesExceptionEnum.BODY_REQUEST_INVALIDO_EXCEPTION)
        
        return gera_json_exception_generica(moovies_exception, exception)
