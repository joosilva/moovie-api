from enum import Enum

class RouterResponseEnum(Enum):
    
    SENHA_ATUALIZADA = ("Senha Atualizada com Sucesso.")
    
    TITULO_AVALIADO = ("Título Avaliado com Sucesso.")
    
    
    def __init__(self, mensagem):
        self._mensagem = mensagem
        
        
    @property
    def mensagem(self):
        return self._mensagem
    