import random

from faker import Faker

from typing import List

from src.domain.dto.avaliacao_dto import AvaliacaoDTO
from src.domain.dto.cineasta_dto import CineastaDTO
from src.domain.dto.filme_dto import FilmeDTO
from src.domain.dto.login_dto import LoginDTO
from src.domain.dto.serie_dto import SerieDTO
from src.domain.dto.temporada_dto import TemporadaDTO
from src.domain.dto.titulo_dto import TituloDTO
from src.domain.dto.token_dto import TokenDTO
from src.domain.dto.usuario_new_dto import UsuarioNewDTO

from src.domain.enums.genero_titulo_enum import GeneroTituloEnum

from src.domain.service.auth_service import AuthService
from src.domain.service.avaliacao_service import AvaliacaoService
from src.domain.service.cineasta_service import CineastaService
from src.domain.service.filme_service import FilmeService
from src.domain.service.serie_service import SerieService
from src.domain.service.usuario_service import UsuarioService

from src.config.database import DatabaseConfig

db = DatabaseConfig()

class DataGenerator:
    
    def __enter__(self):
        self.db_context = db.session_scope()
        self.db = self.db_context.__enter__()

        self.auth_service = AuthService(self.db)
        self.avaliacao_service = AvaliacaoService(self.db)
        self.cineasta_service = CineastaService(self.db)
        self.filme_service = FilmeService(self.db)
        self.serie_service = SerieService(self.db)
        self.usuario_service = UsuarioService(self.db)

        self.fake = Faker("pt_BR")
        self.tokens_por_usuario = {}
        
        return self

    
    def generate(self):
        if self._is_dados_ja_existem():
            return

        print("Gerando dados iniciais...")
        self.generate_usuarios()
        self.generate_cineastas()
        self.generate_filmes()
        self.generate_series()
        print("Dados gerados com sucesso!")

    
    def generate_usuarios(self):
        usuarios = []

        usuarios.append(UsuarioNewDTO(
            nome = "Moovies API",
            username = "moovies-api",
            email = "moovies-api@python.com",
            senha = "python@MooviesApi159"
        ))
        
        for i in range(1, 21):
            usuarios.append(UsuarioNewDTO(
                nome = f"Usuário {i}",
                username = f"usuario{i}",
                email = f"usuario{i}@python.com",
                senha = f"usuario{i}"
            ))

        for usuario in usuarios:
            
            usuario: UsuarioNewDTO = usuario
            
            senha_usuario = usuario.senha
            self.usuario_service.cria_novo_usuario(usuario)
            usuario.senha = senha_usuario
            
            login_dto = LoginDTO(username = usuario.username, senha = usuario.senha)
            token: TokenDTO = self.auth_service.loga_usuario(login_dto, duracao_token = 30)

            self.tokens_por_usuario[usuario.username] = token.token

    
    def generate_cineastas(self):
        cineastas_dto: List[CineastaDTO] = []
        
        self.cineastas_ids_por_cargo = {
            "Diretor(a)": [],
            "Ator/Atriz": [],
            "Roteirista": [],
            "Editor(a)": []
        }

        cargos = list(self.cineastas_ids_por_cargo.keys())
        
        for cargo in cargos:
            nome = self.fake.name()
            cineasta_dto = CineastaDTO(nome = nome, cargo = cargo)
            
            cineastas_dto.append(cineasta_dto)

        for _ in range(200 - len(cargos)):
            nome = self.fake.name()
            cargo = random.choice(cargos)

            cineasta_dto = CineastaDTO(nome = nome, cargo = cargo)
            
            cineastas_dto.append(cineasta_dto)
            
        cineastas_criados = self.cineasta_service.cria_novos_cineastas(cineastas_dto)
        
        for cineasta_criado in cineastas_criados:
            self.cineastas_ids_por_cargo[cineasta_criado.cargo].append((cineasta_criado.id_cineasta, cineasta_criado.nome))

    
    def generate_filmes(self):
        filmes: List[FilmeDTO] = []
        
        for i in range(100):
            genero = random.choice(GeneroTituloEnum.lista())[1]
            
            titulo_nome = f"Filme {i+1}: {self.fake.sentence(nb_words = 3)}"

            elenco_ids = self._gera_elenco()
            elenco_dto = [self._cineasta_dto_by_id(id_) for id_ in elenco_ids]
            
            titulo_dto = TituloDTO(
                titulo = titulo_nome,
                descricao = self.fake.text(),
                duracao_minutos = random.randint(80, 180),
                data_lancamento = self.fake.date_time_between(start_date = "-10y", end_date = "now"),
                elenco = elenco_dto
            )

            filme_dto = FilmeDTO(
                genero = genero,
                filme = titulo_dto
            )

            filmes.append(filme_dto)
            
        filmes_criados = self.filme_service.cria_novos_filmes(filmes)
        
        for filme_criado in filmes_criados:
            self._gera_avaliacoes_para_filme(filme_criado.id_filme)
            


    
    def generate_series(self):
        series: List[SerieDTO] = []
        
        for i in range(100):
            genero = random.choice(GeneroTituloEnum.lista())[1]
            
            titulo = f"Série {i+1}: {self.fake.sentence(nb_words = 3)}"

            temporadas = []
            num_temporadas = random.randint(1, 5)
            elenco_principal_ids = self._gera_elenco()

            for num in range(1, num_temporadas + 1):
                episodios = []
                
                qtd_episodios = random.randint(3, 10)

                for ep in range(qtd_episodios):
                    elenco_atores_disponiveis = list(set(self.cineastas_ids_por_cargo["Ator/Atriz"]) - set(elenco_principal_ids))
                    elenco_adicional_ids = random.sample(elenco_atores_disponiveis, min(len(elenco_atores_disponiveis), random.randint(1, 3)))
                    elenco_episodio_ids = elenco_principal_ids + elenco_adicional_ids
                    
                    elenco_dto = [self._cineasta_dto_by_id(id_) for id_ in elenco_episodio_ids]

                    titulo_dto = TituloDTO(
                        titulo = f"Episódio {ep+1}",
                        descricao = self.fake.text(),
                        duracao_minutos = random.randint(20, 60),
                        data_lancamento = self.fake.date_time_between(start_date = "-5y", end_date = "now"),
                        elenco = elenco_dto
                    )
                    episodios.append(titulo_dto)

                temporada = TemporadaDTO(
                    numero_temporada = num,
                    qtd_episodios = len(episodios),
                    data_lancamento = self.fake.date_time_between(start_date = "-5y", end_date = "now"),
                    episodios = episodios
                )

                temporadas.append(temporada)

            serie_dto = SerieDTO(
                titulo = titulo,
                genero = genero,
                temporadas = temporadas
            )

            series.append(serie_dto)
            
        series_criadas = self.serie_service.cria_novas_series(series)
        
        for serie_criada in series_criadas:
            self._gera_avaliacoes_para_serie(serie_criada.id_serie)


    def _is_dados_ja_existem(self):
        return (
            self.filme_service.count_filmes() > 0
            or
            self.serie_service.count_series() > 0
            or
            self.usuario_service.count_usuarios() > 0
        )

    
    def _gera_elenco(self):
        diretor = random.choice(self.cineastas_ids_por_cargo["Diretor(a)"])
        roteirista = random.choice(self.cineastas_ids_por_cargo["Roteirista"])
        editor = random.choice(self.cineastas_ids_por_cargo["Editor(a)"])
        
        atores = random.sample(self.cineastas_ids_por_cargo["Ator/Atriz"], random.randint(2, 5))

        elenco = [diretor] + atores + [roteirista, editor]
        
        return elenco

    
    def _todos_cineastas_ids(self):
        return sum(self.cineastas_ids_por_cargo.values(), [])

    
    def _cineasta_dto_by_id(self, id_):
        for cargo, cineastas in self.cineastas_ids_por_cargo.items():
            for cineasta_id, nome in cineastas:
                if cineasta_id == id_:
                    return CineastaDTO(id_cineasta = id_, nome = nome, cargo = cargo)

    
    def _gera_avaliacoes_para_filme(self, id_filme):
        qtd_avaliacoes = random.randint(5, 15)
        
        usuarios = list(self.tokens_por_usuario.values())
        
        for token in random.sample(usuarios, qtd_avaliacoes):
            nota = random.randint(1, 5)
            self.avaliacao_service.avalia_filme(id_filme, AvaliacaoDTO(nota = nota), token)

    
    def _gera_avaliacoes_para_serie(self, id_serie):
        qtd_avaliacoes = random.randint(5, 15)
        
        usuarios = list(self.tokens_por_usuario.values())
        
        for token in random.sample(usuarios, qtd_avaliacoes):
            nota = random.randint(1, 5)
            self.avaliacao_service.avalia_serie(id_serie, AvaliacaoDTO(nota = nota), token)
    
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.db_context.close()
        except Exception:
            pass
