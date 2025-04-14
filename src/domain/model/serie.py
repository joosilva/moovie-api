from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from src.config.database import Base

class Serie(Base):
    
    __tablename__ = "series"
    
    id_serie = Column(Integer, primary_key = True, autoincrement = True)
    id_genero = Column(Integer, nullable = False)
    titulo = Column(String, nullable = False)
    data_inativacao = Column(DateTime, nullable = True)
    
    temporadas = relationship("Temporada", back_populates = "serie", cascade = "all, delete-orphan")
    
    avaliacoes = relationship("Avaliacao", back_populates = "serie", uselist = True)


    def to_dto(self):
        from typing import List
        
        from src.domain.dto.avaliacao_dto import AvaliacaoDTO
        from src.domain.dto.serie_dto import SerieDTO
        from src.domain.dto.temporada_dto import TemporadaDTO
        from src.domain.model.avaliacao import Avaliacao
        from src.domain.model.temporada import Temporada
        from src.domain.enums.genero_titulo_enum import GeneroTituloEnum
        
        genero: str = GeneroTituloEnum.descricao_from_id(self.id_genero)
        
        temporadas: List[TemporadaDTO] = []
        for temporada in self.temporadas:
            temporada: Temporada = temporada
            
            temporadas.append(temporada.to_dto())
            
        avaliacoes_dto: List[AvaliacaoDTO] = []
        if self.avaliacoes is not None:
            for avaliacao in self.avaliacoes:
                avaliacao: Avaliacao = avaliacao
                
                avaliacoes_dto.append(avaliacao.to_dto())
        
        return SerieDTO(
            id_serie = self.id_serie,
            titulo = self.titulo,
            genero = genero,
            temporadas = temporadas,
            avaliacao = avaliacoes_dto
        )
