from enum import Enum

class GeneroTituloEnum(Enum):
    
    ACAO = (1, "Ação")
    COMEDIA = (2, "Comédia")
    ROMANCE = (3, "Romance")
    SUSPENSE = (4, "Suspense")
    TERROR = (5, "Terror")
    
    
    def __init__(self, id_genero: int, descricao: str):
        self._id_genero = id_genero
        self._descricao = descricao
        
    
    @property
    def id_genero(self):
        return self._id_genero
    
    
    @property
    def descricao(self):
        return self._descricao
    
    
    @classmethod
    def lista(cls):
        return [(e.value[0], e.value[1]) for e in cls]
    
    
    @classmethod
    def id_from_descricao(cls, descricao) -> int:
        for tipo in cls:
            if tipo.descricao == descricao:
                return tipo.id_genero
            
        return None
    
    
    @classmethod
    def descricao_from_id(cls, id_genero) -> str:
        for tipo in cls:
            if tipo.id_genero == id_genero:
                return tipo.descricao
            
        return None
    