from pydantic import BaseModel

class LoginDTO(BaseModel):
    
    username: str
    senha: str
