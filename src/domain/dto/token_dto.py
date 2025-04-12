from datetime import datetime
from pydantic import BaseModel

class TokenDTO(BaseModel):
    
    token: str
    data_expiracao: datetime
    