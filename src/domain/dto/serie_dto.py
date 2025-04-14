from pydantic import BaseModel
from typing import Optional

from typing import List

from src.domain.dto.avaliacao_dto import AvaliacaoDTO
from src.domain.dto.temporada_dto import TemporadaDTO

class SerieDTO(BaseModel):
    
    id_serie: Optional[int] = None
    titulo: str
    genero: str
    
    temporadas: List[TemporadaDTO]
    
    avaliacoes: Optional[List[AvaliacaoDTO]] = None
    
    
    def to_model(self):
        from src.domain.enums.genero_titulo_enum import GeneroTituloEnum
        from src.domain.model.avaliacao import Avaliacao
        from src.domain.model.serie import Serie
        
        id_genero: int = GeneroTituloEnum.id_from_descricao(self.genero)
        
        avaliacoes_model: List[Avaliacao] = []
        if self.avaliacoes is not None:
            for avaliacao in self.avaliacoes:
                avaliacao: AvaliacaoDTO = avaliacao
                
                avaliacoes_model.append(avaliacao.to_model())
        
        return Serie(
            titulo = self.titulo,
            id_genero = id_genero,
            avaliacoes = avaliacoes_model,
            temporadas = [temporada.to_model() for temporada in self.temporadas] 
        )
