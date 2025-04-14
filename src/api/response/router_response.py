import json

from pydantic import BaseModel

from src.api.response.enums.router_response_enum import RouterResponseEnum

class RouterResponse(BaseModel):
    
    mensagem: str
    
    
    def __init__(self, response_enum: RouterResponseEnum):
        self.mensagem = response_enum.mensagem
        
        
    def __str__(self):
        response = {
            "mensagem": self.mensagem
        }
        
        return json.dumps(response)
    
