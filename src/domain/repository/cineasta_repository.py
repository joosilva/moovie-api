from src.domain.model.cineasta import Cineasta
from src.domain.repository.base.base_repository import BaseRepository

class CineastaRepository(BaseRepository):
    
    def cria_novo_cineasta(self, cineasta: Cineasta) -> Cineasta:
        self.db.add(cineasta)
        self.db.commit()
        self.db.refresh(cineasta)
        
        return cineasta