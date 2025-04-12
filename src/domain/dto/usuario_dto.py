from pydantic import BaseModel
from typing import Optional

class UsuarioDTO(BaseModel):
    
    id_usuario: int
    nome: str
    username: str
    email: str
