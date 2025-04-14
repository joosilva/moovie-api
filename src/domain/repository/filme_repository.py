from typing import List

from sqlalchemy import func
from sqlalchemy.orm import aliased, contains_eager, joinedload

from src.domain.model.avaliacao import Avaliacao
from src.domain.model.cineasta import Cineasta
from src.domain.model.filme import Filme
from src.domain.model.titulo import Titulo
from src.domain.repository.base.base_repository import BaseRepository

class FilmeRepository(BaseRepository):
    
    def count_filmes(self) -> int:
        return self.db.query(Filme).count()
    
    
    def cria_novo_filme(self, filme: Filme) -> Filme:
        titulo: Titulo = filme.filme

        elenco_completo: List[Cineasta] = []

        for cineasta in titulo.elenco:
            cineasta: Cineasta = cineasta

            cineasta_obj = self.db.query(Cineasta).filter(Cineasta.id_cineasta == cineasta.id_cineasta).first()

            if cineasta_obj:
                elenco_completo.append(cineasta_obj)

        titulo.elenco = elenco_completo
        
        self.db.add(filme)
        self.db.commit()
        self.db.refresh(filme)
        
        return filme
    
    
    def busca_filme_by_id(self, id_filme: int) -> Filme:
        filme = self.db.query(Filme).filter_by(id_filme = id_filme).first()
        
        return filme
    
    
    def busca_filmes_e_avaliacoes_usuario(self, id_usuario: int) -> List[Filme]:
        avaliacao_alias = aliased(Avaliacao)

        filmes = (
            self.db.query(Filme)
            .join(Filme.filme)
            .outerjoin(avaliacao_alias,
                        (avaliacao_alias.id_filme == Filme.id_filme) & 
                        (avaliacao_alias.id_usuario == id_usuario))
            .options(
                contains_eager(Filme.avaliacoes, alias=avaliacao_alias),
                joinedload(Filme.filme).joinedload(Titulo.elenco)  
            )
            .filter(Filme.data_inativacao == None)
            .all()
        )

        return filmes
    
    
    def busca_filmes_filtragem_conteudo(self, id_usuario: int, qtd_recomendacoes: int) -> List[Filme]:
        top_filmes_avaliados = (
            self.db.query(Filme, func.max(Avaliacao.nota).label("nota_maxima"))
            .join(Avaliacao, Avaliacao.id_filme == Filme.id_filme)
            .filter(Avaliacao.id_usuario == id_usuario)
            .filter(Avaliacao.id_serie == None)
            .group_by(Filme.id_filme)
            .order_by(func.max(Avaliacao.nota).desc()) 
            .limit(5)
            .all()
        )

        if not top_filmes_avaliados:
            return None

        generos_avaliados = {filme.filme.id_genero for filme, _ in top_filmes_avaliados}

        cineastas_avaliados = set()
        for filme, _ in top_filmes_avaliados:
            for cineasta in filme.filme.elenco:
                cineastas_avaliados.add(cineasta.id_cineasta)

        filmes_filtrados = (
            self.db.query(Filme)
            .join(Titulo, Filme.id_filme == Titulo.id_filme)
            .join(Titulo.elenco)
            .filter(Filme.data_inativacao == None)
            .filter(Filme.filme.id_genero.in_(generos_avaliados))
            .filter(Filme.id_filme.notin_([filme.id_filme for filme, _ in top_filmes_avaliados]))
            .filter(Titulo.elenco.any(Cineasta.id_cineasta.in_(cineastas_avaliados)))  
            .distinct()
            .limit(qtd_recomendacoes)
            .all()
        )

        return filmes_filtrados
    
    
    def busca_filmes_filtragem_colaborativa(self, qtd_recomendacoes: int) -> List[Filme]:
        top_filmes_avaliados_colaborativo = (
            self.db.query(Filme, func.max(Avaliacao.nota).label("nota_maxima"), func.count(Avaliacao.id_filme).label("num_avaliacoes"))
            .join(Avaliacao, Avaliacao.id_filme == Filme.id_filme)
            .filter(Avaliacao.id_serie == None)
            .group_by(Filme.id_filme)
            .order_by(func.count(Avaliacao.id_filme).desc(), func.max(Avaliacao.nota).desc())
            .all()
        )

        if not top_filmes_avaliados_colaborativo:
            return None
        
        generos_avaliados = {filme.filme.id_genero for filme, _, _ in top_filmes_avaliados_colaborativo}

        cineastas_avaliados = set()
        for filme, _, _ in top_filmes_avaliados_colaborativo:
            for cineasta in filme.filme.elenco:
                cineastas_avaliados.add(cineasta.id_cineasta)

        filmes_filtrados = (
            self.db.query(Filme)
            .join(Titulo, Filme.id_filme == Titulo.id_filme)
            .join(Titulo.elenco)
            .filter(Filme.data_inativacao == None) 
            .filter(Filme.filme.id_genero.in_(generos_avaliados))
            .filter(Filme.id_filme.notin_([filme.id_filme for filme, _, _ in top_filmes_avaliados_colaborativo]))
            .filter(Titulo.elenco.any(Cineasta.id_cineasta.in_(cineastas_avaliados)))
            .distinct()
            .limit(qtd_recomendacoes)
            .all()
        )

        return filmes_filtrados
