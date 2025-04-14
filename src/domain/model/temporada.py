from sqlalchemy import Column, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship

from src.config.database import Base

class Temporada(Base):
    
    __tablename__ = "temporadas"
    
    id_temporada = Column(Integer, primary_key = True, autoincrement = True)
    numero_temporada = Column(Integer, nullable = False)
    qtd_episodios = Column(Integer, nullable = False)
    data_lancamento = Column(DateTime, nullable = False)
    
    id_serie = Column(Integer, ForeignKey("series.id_serie"), nullable = False)
    serie = relationship("Serie", back_populates = "temporadas")
    
    episodios = relationship("Titulo", back_populates = "temporada", cascade = "all, delete-orphan")
    
    
    def to_dto(self):
        from typing import List
        
        from src.domain.dto.temporada_dto import TemporadaDTO
        from src.domain.dto.titulo_dto import TituloDTO
        from src.domain.model.titulo import Titulo
        
        episodios: List[TituloDTO] = []
        for episodio in self.episodios:
            episodio: Titulo = episodio
            
            episodios.append(episodio.to_dto())
        
        return TemporadaDTO(
            id_temporada = self.id_temporada,
            numero_temporada = self.numero_temporada,
            qtd_episodios = len(episodios),
            data_lancamento = self.data_lancamento,
            episodios = episodios
        )
    