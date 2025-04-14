from sqlalchemy import Column, ForeignKey, Integer

from src.config.database import Base

class TituloElenco(Base):
    
    __tablename__ = "titulo_elenco"
    
    id_titulo = Column(Integer, ForeignKey("titulos.id_titulo"), primary_key = True)
    id_cineasta = Column(Integer, ForeignKey("cineastas.id_cineasta"), primary_key = True)
