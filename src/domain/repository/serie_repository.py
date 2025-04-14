from typing import List

from sqlalchemy import func
from sqlalchemy.orm import aliased, contains_eager

from src.domain.model.avaliacao import Avaliacao
from src.domain.model.cineasta import Cineasta
from src.domain.model.serie import Serie
from src.domain.model.temporada import Temporada
from src.domain.model.titulo import Titulo
from src.domain.repository.base.base_repository import BaseRepository

class SerieRepository(BaseRepository):
    
    def count_series(self) -> int:
        return self.db.query(Serie).count()
    
    
    def cria_nova_serie(self, serie: Serie) -> Serie:
        for temporada in serie.temporadas:
            for episodio in temporada.episodios:
                
                elenco_completo = []

                for cineasta in episodio.elenco:
                    cineasta_obj = self.db.query(Cineasta).filter(Cineasta.id_cineasta == cineasta.id_cineasta).first()

                    if cineasta_obj:
                        elenco_completo.append(cineasta_obj)

                episodio.elenco = elenco_completo
                
            self.db.add(temporada)

        self.db.add(serie)
        self.db.commit()
        self.db.refresh(serie)
        
        return serie
    
    
    def busca_serie_by_id(self, id_serie: int) -> Serie:
        serie = self.db.query(Serie).filter_by(id_serie = id_serie).first()
        
        return serie   
    
    
    def busca_series_e_avaliacoes_usuario(self, id_usuario: int) -> List[Serie]:
        avaliacao_alias = aliased(Avaliacao)

        series = (
            self.db.query(Serie)
            .outerjoin(avaliacao_alias, 
                    (avaliacao_alias.id_serie == Serie.id_serie) &
                    (avaliacao_alias.id_usuario == id_usuario))
            .options(
                contains_eager(Serie.avaliacoes, alias=avaliacao_alias)
            )
            .filter(Serie.data_inativacao == None)
            .all()
        )

        return series
    
    
    def busca_series_filtragem_conteudo(self, id_usuario: int, qtd_recomendacoes: int) -> List[Serie]:
        top_series_avaliadas = (
            self.db.query(Serie, func.max(Avaliacao.nota).label("nota_maxima"))
            .join(Avaliacao, Avaliacao.id_serie == Serie.id_serie)
            .filter(Avaliacao.id_usuario == id_usuario)
            .filter(Avaliacao.id_filme == None)
            .group_by(Serie.id_serie)
            .order_by(func.max(Avaliacao.nota).desc())
            .limit(5)
            .all()
        )

        if not top_series_avaliadas:
            return None

        generos_avaliados = {serie.id_genero for serie, _ in top_series_avaliadas}

        cineastas_avaliados = set()
        for serie, _ in top_series_avaliadas:
            for temporada in serie.temporadas:
                for episodio in temporada.episodios:
                    for cineasta in episodio.elenco:
                        cineastas_avaliados.add(cineasta.id_cineasta)

        series_filtradas = (
            self.db.query(Serie)
            .join(Temporada, Serie.id_serie == Temporada.id_serie)
            .join(Temporada.episodios)
            .join(Titulo.elenco)
            .filter(Serie.data_inativacao == None)
            .filter(Serie.id_genero.in_(generos_avaliados))
            .filter(Serie.id_serie.notin_([serie.id_serie for serie, _ in top_series_avaliadas]))
            .filter(Titulo.elenco.any(Cineasta.id_cineasta.in_(cineastas_avaliados)))
            .distinct()
            .limit(qtd_recomendacoes)
            .all()
        )

        return series_filtradas
    
    
    def busca_series_filtragem_colaborativa(self, qtd_recomendacoes: int) -> List[Serie]:
        top_series_avaliadas = (
            self.db.query(Serie, func.max(Avaliacao.nota).label("nota_maxima"), func.count(Avaliacao.id_serie).label("num_avaliacoes"))
            .join(Avaliacao, Avaliacao.id_serie == Serie.id_serie)
            .filter(Avaliacao.id_filme == None)
            .group_by(Serie.id_serie)
            .order_by(func.count(Avaliacao.id_serie).desc(), func.max(Avaliacao.nota).desc())
            .all()
        )

        if not top_series_avaliadas:
            return None

        generos_avaliados = {serie.id_genero for serie, _, _ in top_series_avaliadas}

        cineastas_avaliados = set()
        for serie, _, _ in top_series_avaliadas:
            for temporada in serie.temporadas:
                for episodio in temporada.episodios:
                    for cineasta in episodio.elenco:
                        cineastas_avaliados.add(cineasta.id_cineasta)

        series_filtradas = (
            self.db.query(Serie)
            .join(Temporada, Serie.id_serie == Temporada.id_serie)
            .join(Temporada.episodios)
            .join(Titulo.elenco)
            .filter(Serie.data_inativacao == None)
            .filter(Serie.id_genero.in_(generos_avaliados))
            .filter(Serie.id_serie.notin_([serie.id_serie for serie, _, _ in top_series_avaliadas]))
            .filter(Titulo.elenco.any(Cineasta.id_cineasta.in_(cineastas_avaliados)))
            .distinct()
            .limit(qtd_recomendacoes)
            .all()
        )

        return series_filtradas
