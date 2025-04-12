from src.api.exceptions.moovies_exception import MooviesException
from src.domain.exceptions.enums.moovies_exception_enum import MooviesExceptionEnum

class LoginInvalidoException(MooviesException):
    
    def __init__(self):
        super().__init__(MooviesExceptionEnum.LOGIN_INVALIDO_EXCEPTION)
        

class LoginVazioException(MooviesException):
    
    def __init__(self):
        super().__init__(MooviesExceptionEnum.LOGIN_VAZIO_EXCEPTION)


class SenhaDivergenteException(MooviesException):
    
    def __init__(self):
        super().__init__(MooviesExceptionEnum.SENHA_DIVERGENTE_EXCEPTION)


class TokenExpiradoException(MooviesException):
    
    def __init__(self):
        super().__init__(MooviesExceptionEnum.TOKEN_EXPIRADO_EXCEPTION)


class TokenInvalidoException(MooviesException):
    
    def __init__(self):
        super().__init__(MooviesExceptionEnum.TOKEN_INVALIDO_EXCEPTION)


class TokenVazioException(MooviesException):
    
    def __init__(self):
        super().__init__(MooviesExceptionEnum.TOKEN_VAZIO_EXCEPTION)
        
        
class UsuarioInvalidoException(MooviesException):
    
    def __init__(self):
        super().__init__(MooviesExceptionEnum.USUARIO_INVALIDO_EXCEPTION)
        

class UsuarioExistenteException(MooviesException):
    
    def __init__(self):
        super().__init__(MooviesExceptionEnum.USUARIO_JA_EXISTENTE_EXCEPTION)
