from pydantic import BaseModel

class MooviesExceptionResponse(BaseModel):
    
    exception: str
    mensagem: str
