from typing import List

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.orm import relationship

from src.config.database import Base

class Filme(Base):
    
    __tablename__ = "filmes"
    
    id_filme = Column(Integer, primary_key = True, autoincrement = True)
    id_genero = Column(Integer, nullable = False)
    data_inativacao = Column(DateTime, nullable = True)
    
    filme = relationship("Titulo", back_populates = "filme", uselist = False)
    
    avaliacoes = relationship("Avaliacao", back_populates = "filme", uselist = True)
    
    
    def to_dto(self):
        from src.domain.dto.avaliacao_dto import AvaliacaoDTO
        from src.domain.dto.filme_dto import FilmeDTO
        from src.domain.model.avaliacao import Avaliacao
        from src.domain.model.titulo import Titulo
        from src.domain.enums.genero_titulo_enum import GeneroTituloEnum
        
        genero: str = GeneroTituloEnum.descricao_from_id(self.id_genero)
        filme: Titulo = self.filme
        
        avaliacoes_dto: List[AvaliacaoDTO] = []
        if self.avaliacoes is not None:
            for avaliacao in self.avaliacoes:
                avaliacao: Avaliacao = avaliacao
                
                avaliacoes_dto.append(avaliacao.to_dto())
        
        return FilmeDTO(
            id_filme = self.id_filme,
            genero = genero,
            filme = filme.to_dto(),
            avaliacao = avaliacoes_dto
        )
            