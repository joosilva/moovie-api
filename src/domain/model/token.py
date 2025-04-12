from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from datetime import datetime, timedelta

from src.config.database import Base

class Token(Base):
    
    __tablename__ = "tokens"

    token = Column(String, primary_key = True, unique = True, index = True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"))
    
    data_criacao = Column(DateTime, default = datetime.now())
    data_expiracao = Column(DateTime, default = lambda: datetime.now() + timedelta(minutes = 30))
    data_logout = Column(DateTime, nullable = True)
    
    usuario = relationship("Usuario", back_populates="tokens")
    
    def is_expirado(self):
        return self.data_expiracao < datetime.now()
    
    def to_dto(self):
        from src.domain.dto.token_dto import TokenDTO
        
        return TokenDTO(
            token = self.token if self.token.startswith("Bearer ") else "Bearer " + self.token, 
            data_expiracao = self.data_expiracao
        )
    