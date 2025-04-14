from sqlalchemy.orm import Session

from src.domain.dto.avaliacao_dto import AvaliacaoDTO
from src.domain.repository.avaliacao_repository import AvaliacaoRepository
from src.domain.service.base.base_service import BaseService
from src.domain.service.filme_service import FilmeService
from src.domain.service.serie_service import SerieService
from src.domain.service.usuario_service import UsuarioService

class AvaliacaoService(BaseService):
    
    def __init__(self, db: Session):
        self.db = db
        self.filme_service = FilmeService(db)
        self.serie_service = SerieService(db)
        self.usuario_service = UsuarioService(db)
        self.avaliacao_repository = AvaliacaoRepository(db)
        
    
    def avalia_filme(self, id_filme: int, avaliacao: AvaliacaoDTO, token_code: str):
        id_usuario = self.usuario_service.recupera_id_usuario_by_token(token_code)

        self.filme_service.valida_filme_existente_by_id(id_filme)
        
        self.avaliacao_repository.registra_avaliacao_filme(id_filme, avaliacao.valida_nota(), id_usuario)
        
    
    def atualiza_avaliacao_filme(self, id_filme: int, avaliacao: AvaliacaoDTO, token_code: str):
        id_usuario = self.usuario_service.recupera_id_usuario_by_token(token_code)

        self.filme_service.valida_filme_existente_by_id(id_filme)
        
        self.avaliacao_repository.atualiza_avaliacao_filme(id_filme, avaliacao.valida_nota(), id_usuario)
        
    
    def avalia_serie(self, id_serie: int, avaliacao: AvaliacaoDTO, token_code: str):
        id_usuario = self.usuario_service.recupera_id_usuario_by_token(token_code)

        self.serie_service.valida_serie_existente_by_id(id_serie)
        
        self.avaliacao_repository.registra_avaliacao_serie(id_serie, avaliacao.valida_nota(), id_usuario)
        
    
    def atualiza_avaliacao_serie(self, id_serie: int, avaliacao: AvaliacaoDTO, token_code: str):
        id_usuario = self.usuario_service.recupera_id_usuario_by_token(token_code)

        self.serie_service.valida_serie_existente_by_id(id_serie)
        
        self.avaliacao_repository.atualiza_avaliacao_serie(id_serie, avaliacao.valida_nota(), id_usuario)
