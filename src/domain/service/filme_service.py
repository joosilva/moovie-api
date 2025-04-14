from typing import List

from sqlalchemy.orm import Session

from src.domain.dto.filme_dto import FilmeDTO
from src.domain.exceptions.exceptions import TituloNaoEncontradoException
from src.domain.model.filme import Filme
from src.domain.repository.filme_repository import FilmeRepository
from src.domain.service.base.base_service import BaseService
from src.domain.service.usuario_service import UsuarioService

class FilmeService(BaseService):
    
    def __init__(self, db: Session):
        self.db = db
        self.usuario_service = UsuarioService(db)
        self.filme_repository = FilmeRepository(db)
        
    
    def count_filmes(self) -> int:
        return self.filme_repository.count_filmes()
    
    
    def cria_novos_filmes(self, filmes: List[FilmeDTO]) -> List[FilmeDTO]:
        filmes_dto: List[FilmeDTO] = []
        
        for filme in filmes:
            filme = self.filme_repository.cria_novo_filme(filme.to_model())
            
            filmes_dto.append(filme.to_dto())
            
        return filmes_dto
    
        
    def cria_novo_filme(self, filme: FilmeDTO) -> FilmeDTO:
        novo_filme = self.filme_repository.cria_novo_filme(filme.to_model())
        
        return novo_filme.to_dto() 
        
        
    def valida_filme_existente_by_id(self, id_filme: int):
        filme: Filme = self.filme_repository.busca_filme_by_id(id_filme)
        
        if not filme:
            raise TituloNaoEncontradoException()
        
    
    def recupera_id_usuario(self, token_code: str):
        return self.usuario_service.recupera_id_usuario_by_token(token_code)
    
        
    def busca_filmes_e_avaliacoes_usuario(self, token_code: str) -> List[FilmeDTO]:
        id_usuario = self.recupera_id_usuario(token_code)
        
        filmes = self.filme_repository.busca_filmes_e_avaliacoes_usuario(id_usuario)
        
        filmes_dto: List[FilmeDTO] = []
        for filme in filmes:
            filme: Filme = filme
            
            filmes_dto.append(filme.to_dto())
            
        return filmes_dto
    
    
    def busca_filmes_recomendados_usuario(self, token_code: str, qtd_recomendacoes: int) -> List[FilmeDTO]:
        id_usuario = self.recupera_id_usuario(token_code)
        
        recomendacoes = self.filme_repository.busca_filmes_filtragem_conteudo(id_usuario, qtd_recomendacoes)
        
        qtd_filmes = len(recomendacoes)
        if qtd_filmes < qtd_recomendacoes:
            
            qtd_recomendacoes -= qtd_filmes
            
            recomendacoes.append(
                self.filme_repository.busca_filmes_filtragem_colaborativa(qtd_recomendacoes))
            
        filmes_dto: List[FilmeDTO] = []
        for filme in recomendacoes:
            filme: Filme = filme
            
            filmes_dto.append(filme.to_dto())
            
        return filmes_dto
