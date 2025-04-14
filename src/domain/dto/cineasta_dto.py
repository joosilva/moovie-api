from pydantic import BaseModel
from typing import Optional

class CineastaDTO(BaseModel):
    
    id_cineasta: Optional[int] = None
    nome: str
    cargo: str


    def to_model(self):
        from src.domain.enums.tipo_cineasta_enum import TipoCineastaEnum
        from src.domain.model.cineasta import Cineasta
        
        id_tipo = TipoCineastaEnum.id_from_descricao(self.cargo)
        
        return Cineasta(
            id_cineasta = self.id_cineasta,
            nome = self.nome,
            id_tipo = id_tipo
        )