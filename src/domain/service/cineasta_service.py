from typing import List

from sqlalchemy.orm import Session

from src.domain.dto.cineasta_dto import CineastaDTO
from src.domain.model.cineasta import Cineasta
from src.domain.repository.cineasta_repository import CineastaRepository
from src.domain.service.base.base_service import BaseService

class CineastaService(BaseService):
    
    def __init__(self, db: Session):
        self.db = db
        self.cineasta_repository = CineastaRepository(db)
        
        
    def cria_novos_cineastas(self, cineastas: List[CineastaDTO]) -> List[CineastaDTO]:
        cineastas_dto: List[CineastaDTO] = []
        
        for cineasta in cineastas:
            cineasta = self.cineasta_repository.cria_novo_cineasta(cineasta.to_model())
            
            cineastas_dto.append(cineasta.to_dto())
            
        return cineastas_dto
