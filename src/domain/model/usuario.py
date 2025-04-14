from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from datetime import datetime

from src.config.database import Base

class Usuario(Base):
        
    __tablename__ = "usuarios"
    
    id_usuario = Column(Integer, primary_key = True, autoincrement = True)
    nome = Column(String, nullable = False)
    username = Column(String, nullable = False)
    email = Column(String, nullable = False)
    senha_hash = Column(String, nullable = False)
    
    data_criacao = Column(DateTime, default = datetime.now())
    data_exclusao = Column(DateTime, nullable = True)
    
    tokens = relationship("Token", back_populates = "usuario")
    
    avaliacoes = relationship("Avaliacao", back_populates = "usuario")
    
    def to_dto(self):
        from src.domain.dto.usuario_dto import UsuarioDTO
        
        usuario = UsuarioDTO(    
            id_usuario = self.id_usuario,
            nome = self.nome,
            username = self.username,
            email = self.email
        )
        
        return usuario
