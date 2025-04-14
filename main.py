from fastapi import FastAPI

#Config:
from src.config.openapi import custom_openapi

#Interceptor/Middleware:
from src.api.interceptor.interceptor import add_request_interceptor

#Rotas da API:
from src.api.router.auth_router import router as auth
from src.api.router.avaliacao_router import router as avaliacao
from src.api.router.filme_router import router as filme
from src.api.router.serie_router import router as serie
from src.api.router.usuario_router import router as usuario

#Exception Handler:
from src.api.exceptions.handler.exception_handlers import exception_handlers

#DataGenerator:
from src.scripts.data_generator import DataGenerator

app = FastAPI()

add_request_interceptor(app)

app.include_router(auth)
app.include_router(avaliacao)
app.include_router(filme) 
app.include_router(serie)
app.include_router(usuario)

exception_handlers(app)

app.openapi = lambda: custom_openapi(app)

with DataGenerator() as data_generator:
    data_generator.generate()
