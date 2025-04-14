from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from src.config.database import Base

from src.domain.model.titulo_elenco import TituloElenco

class Titulo(Base):
    
    __tablename__ = "titulos"
    
    id_titulo = Column(Integer, primary_key = True, autoincrement = True)
    titulo = Column(String, nullable = False)
    descricao = Column(String, nullable = True)
    duracao_minutos = Column(Integer, nullable = False)
    data_lancamento = Column(DateTime, nullable = False)
    data_inativacao = Column(DateTime, nullable = True)
    
    elenco = relationship("Cineasta", secondary = TituloElenco.__table__, back_populates = "titulos")
    
    id_temporada = Column(Integer, ForeignKey("temporadas.id_temporada"), nullable = True)
    temporada = relationship("Temporada", back_populates = "episodios")
    
    id_filme = Column(Integer, ForeignKey("filmes.id_filme"), nullable = True)
    filme = relationship("Filme", back_populates = "filme", uselist = False)
    
    
    def to_dto(self):
        from typing import List
        
        from src.domain.dto.cineasta_dto import CineastaDTO
        from src.domain.model.cineasta import Cineasta
        from src.domain.dto.titulo_dto import TituloDTO
        
        elenco: List[CineastaDTO] = []
        for cineasta in self.elenco:
            cineasta: Cineasta = cineasta
            
            elenco.append(cineasta.to_dto())
        
        return TituloDTO(
            id_titulo = self.id_titulo,
            titulo = self.titulo,
            descricao = self.descricao,
            duracao_minutos = self.duracao_minutos,
            data_lancamento = self.data_lancamento,
            elenco = elenco
        )
