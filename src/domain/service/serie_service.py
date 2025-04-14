from typing import List

from sqlalchemy.orm import Session

from src.domain.dto.serie_dto import SerieDTO
from src.domain.exceptions.exceptions import TituloNaoEncontradoException
from src.domain.model.serie import Serie
from src.domain.repository.serie_repository import SerieRepository
from src.domain.service.base.base_service import BaseService
from src.domain.service.usuario_service import UsuarioService

class SerieService(BaseService):
    
    def __init__(self, db: Session):
        self.db = db
        self.usuario_service = UsuarioService(db)
        self.serie_repository = SerieRepository(db)
        
        
    def count_series(self) -> int:
        return self.serie_repository.count_series()
    
    
    def cria_novas_series(self, series: List[SerieDTO]) -> List[SerieDTO]:
        series_dto: List[SerieDTO] = []
        
        for serie in series:
            serie = self.serie_repository.cria_nova_serie(serie.to_model())
            
            series_dto.append(serie.to_dto())
            
        return series_dto
        
        
    def cria_nova_serie(self, serie: SerieDTO) -> SerieDTO:
        nova_serie = self.serie_repository.cria_nova_serie(serie.to_model())
        
        return nova_serie.to_dto()
        
        
    def valida_serie_existente_by_id(self, id_serie: int):
        serie: Serie = self.serie_repository.busca_serie_by_id(id_serie)
        
        if not serie:
            raise TituloNaoEncontradoException()
        
        
    def busca_series_e_avaliacoes_usuario(self, token_code: str) -> List[SerieDTO]:
        id_usuario = self.usuario_service.recupera_id_usuario_by_token(token_code)
        
        series = self.serie_repository.busca_series_e_avaliacoes_usuario(id_usuario)
        
        series_dto: List[SerieDTO] = []
        for serie in series:
            serie: Serie = serie
            
            series_dto.append(serie.to_dto())
            
        return series_dto
    
    
    def busca_filmes_recomendados_usuario(self, token_code: str, qtd_recomendacoes: int) -> List[SerieDTO]:
        id_usuario = self.recupera_id_usuario(token_code)
        
        recomendacoes = self.serie_repository.busca_series_filtragem_conteudo(id_usuario, qtd_recomendacoes)
        
        qtd_series = len(recomendacoes)
        if qtd_series < qtd_recomendacoes:
            
            qtd_recomendacoes -= qtd_series
            
            recomendacoes.append(
                self.serie_repository.busca_series_filtragem_colaborativa(qtd_recomendacoes))
            
        series_dto: List[SerieDTO] = []
        for serie in recomendacoes:
            serie: Serie = serie
            
            series_dto.append(serie.to_dto())
            
        return series_dto
