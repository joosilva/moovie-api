import json

from src.domain.exceptions.enums.moovies_exception_enum import MooviesExceptionEnum

class MooviesException(Exception):
    
    def __init__(self, moovies_exception_enum: MooviesExceptionEnum):
        self.error = moovies_exception_enum
        
    
    def __str__(self):
        error_response = {
            "exception": self.error.nome,
            "mensagem": self.error.mensagem
        }
        
        return json.dumps(error_response)
