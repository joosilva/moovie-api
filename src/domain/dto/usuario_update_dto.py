from typing import Optional
from pydantic import BaseModel

class UsuarioUpdateDTO(BaseModel):
    
    nome: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    
    def to_model(self, id_usuario_dto: int = None):
        from src.domain.model.usuario import Usuario
        
        usuario = Usuario(
            id_usuario = id_usuario_dto,
            nome = self.nome,
            username = self.username,
            email = self.email
        )
        
        return usuario
