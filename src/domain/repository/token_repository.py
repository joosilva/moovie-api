from datetime import datetime

from src.domain.model.token import Token
from src.domain.repository.base_repository import BaseRepository

class TokenRepository(BaseRepository):
    
    def recupera_token(self, token_code: str) -> Token:
        token = self.db.query(Token).filter(
            Token.token == token_code,
            Token.data_logout.is_(None)
        ).first()
        
        return token
    
    
    def recupera_id_usuario_by_token(self, token_code: str) -> int:
        token = self.recupera_token(token_code)
        
        if token:
            return token.id_usuario
        
        return None
    
    
    def salva_token(self, token: Token):
        self.db.add(token)
        self.db.commit()
        
    
    def inativa_token(self, token_code: str):
        token = self.recupera_token(token_code)
        
        if token:
            token.data_logout = datetime.now()
            
            self.db.commit()
    
    def inativa_token_by_id_usuario(self, id_usuario: int):
        token = self.db.query(Token).filter(
            Token.id_usuario == id_usuario,
            Token.data_logout.is_(None)
        ).order_by(Token.data_expiracao.desc()).first()
        
        if token:
            token.data_logout = datetime.now()
            
            self.db.commit()
