from pydantic import BaseModel, conint

class AvaliacaoDTO(BaseModel):
    
    nota: conint(ge = 1, le = 5)


    def to_model(self):
        from src.domain.model.avaliacao import Avaliacao
        
        return Avaliacao(
            nota = self.nota
        )
    
    
    def valida_nota(self) -> int:
        if self.nota < 1:
            self.nota = 1
            
        if self.nota > 5:
            self.nota = 5
            
        return self.nota
