from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from src.config.database import Base

class Avaliacao(Base):
    
    __tablename__ = "avaliacoes"
    
    id_avaliacao = Column(Integer, primary_key = True, autoincrement = True)
    nota = Column(Integer, nullable = False)
    
    id_filme = Column(Integer, ForeignKey("filmes.id_filme"), nullable = True)
    filme = relationship("Filme", back_populates = "avaliacoes", uselist = True)
    
    id_serie = Column(Integer, ForeignKey("series.id_serie"), nullable = True)
    serie = relationship("Serie", back_populates = "avaliacoes", uselist = True)
    
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable = False)
    usuario = relationship("Usuario", back_populates = "avaliacoes")

    __table_args__ = (
        UniqueConstraint('id_usuario', 'id_filme', name = 'usuario_filme'),
        UniqueConstraint('id_usuario', 'id_serie', name = 'usuario_serie'),
    )
    
    
    def to_dto(self):
        from src.domain.dto.avaliacao_dto import AvaliacaoDTO
        
        return AvaliacaoDTO(
            nota = self.nota
        )
    