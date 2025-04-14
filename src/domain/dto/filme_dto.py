from pydantic import BaseModel
from typing import List, Optional

from src.domain.dto.avaliacao_dto import AvaliacaoDTO
from src.domain.dto.titulo_dto import TituloDTO

class FilmeDTO(BaseModel):
    
    id_filme: Optional[int] = None
    genero: str
    
    filme: TituloDTO
    
    avaliacoes: Optional[List[AvaliacaoDTO]] = None
    
    
    def to_model(self):
        from src.domain.model.filme import Filme
        from src.domain.enums.genero_titulo_enum import GeneroTituloEnum
        
        id_genero: int = GeneroTituloEnum.id_from_descricao(self.genero)
        
        avaliacoes_model: List[AvaliacaoDTO] = []
        if self.avaliacoes is not None: 
            for avaliacao in self.avaliacoes:
                avaliacao: AvaliacaoDTO = avaliacao
                
                avaliacoes_model.append(avaliacao.to_model())
        
        return Filme(
            id_genero = id_genero, 
            filme = self.filme.to_model(), 
            avaliacoes = avaliacoes_model
        )
