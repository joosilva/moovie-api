from pydantic import BaseModel

class UsuarioNewDTO(BaseModel):
    
    nome: str
    username: str
    email: str
    senha: str
    
    def to_model(self):
        from src.domain.model.usuario import Usuario
        
        usuario = Usuario(
            nome = self.nome,
            username = self.username,
            email = self.email,
            senha_hash = self.senha
        )
        
        return usuario
    