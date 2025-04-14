from src.domain.model.avaliacao import Avaliacao
from src.domain.repository.base.base_repository import BaseRepository

class AvaliacaoRepository(BaseRepository):
    
    def registra_avaliacao_filme(self, id_filme: int, nota: int, id_usuario: int):
        avaliacao_existente = self.db.query(Avaliacao).filter_by(id_filme = id_filme, id_usuario = id_usuario).first()
        
        if avaliacao_existente:
            self.atualiza_avaliacao_filme(id_filme, nota, id_usuario)
            
            return
        
        avaliacao = Avaliacao(nota = nota, id_filme = id_filme, id_usuario = id_usuario)
        
        self.db.add(avaliacao)
        self.db.commit()
        

    def atualiza_avaliacao_filme(self, id_filme: int, nota: int, id_usuario: int):
        avaliacao = self.db.query(Avaliacao).filter_by(id_filme = id_filme, id_usuario = id_usuario).first()
        
        if not avaliacao:
            self.registra_avaliacao_filme(id_filme, nota, id_usuario)
            
            return
        
        avaliacao.nota = nota
        
        self.db.commit()
        
        
    def registra_avaliacao_serie(self, id_serie: int, nota: int, id_usuario: int):
        avaliacao_existente = self.db.query(Avaliacao).filter_by(id_serie = id_serie, id_usuario = id_usuario).first()
        
        if avaliacao_existente:
            self.atualiza_avaliacao_serie(id_serie, nota, id_usuario)
            
            return
        
        avaliacao = Avaliacao(nota = nota, id_serie = id_serie, id_usuario = id_usuario)
        
        self.db.add(avaliacao)
        self.db.commit()
    

    def atualiza_avaliacao_serie(self, id_serie: int, nota: int, id_usuario: int):
        avaliacao = self.db.query(Avaliacao).filter_by(id_serie = id_serie, id_usuario = id_usuario).first()
        
        if not avaliacao:
            self.registra_avaliacao_serie(id_serie, nota, id_usuario)
            
            return
        
        avaliacao.nota = nota
        
        self.db.commit()
