from enum import Enum

class MooviesExceptionEnum(Enum):
    
    BODY_REQUEST_INVALIDO_EXCEPTION = (422, "Body Request Inválido", "Body da requisição vazio ou mal formatado.")
    
    LOGIN_INVALIDO_EXCEPTION = (422, "Login Inválido", "Username e/ou senha inválidos.")
    LOGIN_VAZIO_EXCEPTION = (400, "Login Vazio", "Username e senha não fornecidos.")
    
    SENHA_DIVERGENTE_EXCEPTION = (422, "Senha Divergente", "Senha atual diverge da nova senha fornecida.")
    
    TOKEN_EXPIRADO_EXCEPTION = (401, "Token Expirado", "Limite de tempo de expiração do token excedido.")
    TOKEN_INVALIDO_EXCEPTION = (401, "Token Inválido", "Token não é válido.")
    TOKEN_VAZIO_EXCEPTION = (400, "Token Vazio", "Valor de token não fornecido.")
    
    USUARIO_INVALIDO_EXCEPTION = (422, "Usuário Inválido", "Usuário não encontrado.")
    USUARIO_JA_EXISTENTE_EXCEPTION = (422, "Usuário já Existe", "Este username/email já está em uso.")
    
    INTERNAL_SERVER_ERROR = (500, "Internal Server Error", "Erro não tratado pela aplicação.")
    
    
    def __init__(self, status_code: int, nome: str, mensagem: str):
        self._status_code = status_code
        self._nome = nome
        self._mensagem = mensagem
        
    
    @property
    def nome(self):
        return self._nome
        
    
    @property
    def status_code(self):
        return self._status_code

    
    @property
    def mensagem(self):
        return self._mensagem
