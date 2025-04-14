from pydantic import BaseModel

from datetime import datetime
from typing import List, Optional

from src.domain.dto.titulo_dto import TituloDTO

class TemporadaDTO(BaseModel):

    id_temporada: Optional[int] = None
    numero_temporada: int
    qtd_episodios: int
    data_lancamento: datetime
    
    episodios: List[TituloDTO]
    
    
    def to_model(self):
        from src.domain.model.temporada import Temporada
        
        return Temporada(
            numero_temporada = self.numero_temporada,
            qtd_episodios = self.qtd_episodios,
            data_lancamento = self.data_lancamento,
            episodios = [episodio.to_model() for episodio in self.episodios]
        )
