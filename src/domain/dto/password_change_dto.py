from pydantic import BaseModel

class PasswordChangeDTO(BaseModel):
    
    senha_atual: str
    senha_nova: str