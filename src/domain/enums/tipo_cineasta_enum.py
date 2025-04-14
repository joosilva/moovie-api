from enum import Enum

class TipoCineastaEnum(Enum):
    
    DIRECAO = (1, "Diretor(a)")
    ATUACAO = (2, "Ator/Atriz")
    ROTEIRO = (3, "Roteirista")
    EDICAO = (4, "Editor(a)")
    
    
    def __init__(self, id_tipo: int, descricao: str):
        self._id_tipo = id_tipo
        self._descricao = descricao
        
    
    @property
    def id_tipo(self):
        return self._id_tipo
    
    
    @property
    def descricao(self):
        return self._descricao
    
    
    @classmethod
    def lista(cls):
        return [(e.value[0], e.value[1]) for e in cls]
    
    
    @classmethod
    def id_from_descricao(cls, descricao: str) -> int:
        for tipo in cls:
            if tipo.descricao == descricao:
                return tipo.id_tipo
            
        return None
    
    
    @classmethod
    def descricao_from_id(cls, id_tipo: int) -> str:
        for tipo in cls:
            if tipo.id_tipo == id_tipo:
                return tipo.descricao
            
        return None
    