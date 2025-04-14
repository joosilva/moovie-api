from pydantic import BaseModel
from typing import Optional

from datetime import datetime
from typing import List

from src.domain.dto.cineasta_dto import CineastaDTO

class TituloDTO(BaseModel):
    
    id_titulo: Optional[int] = None
    titulo: str
    descricao: str
    duracao_minutos: int
    data_lancamento: datetime
    
    elenco: List[CineastaDTO]
    
    
    def to_model(self):
        from src.domain.model.titulo import Titulo
        
        return Titulo(
            titulo = self.titulo,
            descricao = self.descricao,
            duracao_minutos = self.duracao_minutos,
            data_lancamento = self.data_lancamento,
            elenco = [cineasta.to_model() for cineasta in self.elenco]
        )
    