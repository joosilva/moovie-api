from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.config.database import Base

from src.domain.model.titulo_elenco import TituloElenco

class Cineasta(Base):
    
    __tablename__ = "cineastas"
    
    id_cineasta = Column(Integer, primary_key = True, autoincrement = True)
    nome = Column(String, nullable = False)
    id_tipo = Column(Integer, nullable = False)
    
    titulos = relationship("Titulo", secondary = TituloElenco.__table__, back_populates = "elenco")
    
    
    def to_dto(self):
        from src.domain.dto.cineasta_dto import CineastaDTO
        from src.domain.enums.tipo_cineasta_enum import TipoCineastaEnum
        
        cargo = TipoCineastaEnum.descricao_from_id(self.id_tipo)
        
        return CineastaDTO(
            id_cineasta = self.id_cineasta,
            nome = self.nome,
            cargo = cargo
        )
        
