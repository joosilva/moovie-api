# Moovies API

## Escolha o Idioma(Choose the lenguage):

- [Português](#em-português)
- [English](#in-english)

---

## Em Português

### Visão Geral

Este projeto é a implementação de uma API para uma plataforma de streaming.
O objetivo desta API é permitir que o usuário faça requisições para avaliar filmes e séries e receber indicações de títulos para assistir com base em seus históricos de visualização e preferências.
Este projeto utiliza uma arquitetura em camadas e foi desenvolvido seguindo os princípios de **Clean Architecture, SOLID e Clean Code**, garantindo uma estrutura modular, flexível e escalável..

### Regras

- A API permite criar, modificar e excluir usuários, além de logar e deslogar um usuário;
- Com o usuário criado e logado, um token de acesso é gerado e deve ser usado para realizar as demais requisições;
- A API pode indicar filmes e séries ao usuário realizando uma filtragem colaborativa, recomendando títulos que outros usuários tenham gostado e baseada em conteúdo, analisando parâmetros como avaliações do usuário, gênero, diretores, elenco e recomendando títulos semelhantes. 

### Configuração

O programa é desenvolvido em Python. Existem duas formas de configurar o ambiente para executá-lo:

1. **Instalando Python**:
    - Acesse [aqui](https://www.python.org/downloads/) para baixar o Python e siga as instruções de instalação.
    - Abra o terminal na raíz do projeto e instale as dependências do projeto:
        ```bash
        pip install -r requirements.txt
        ```

2. **Usando Docker (recomendado)**:
    - Acesse [aqui](https://www.docker.com/products/docker-desktop/) para baixar o Docker e siga as instruções de instalação.
    - Abra o Docker e o mantenha rodando.
    - Utilize [GitBash](https://git-scm.com/downloads) para executar os comandos.

#### Configuração Adicional

##### Windows
O projeto possui Dockerfile para configurações e Makefile para executar os comandos Docker. Se você estiver utilizando **Mac Book**, o Makefile irá funcionar corretamente e você pode pular esta seção.

Para Windows, você deve baixar o [GNU Make for Windows](https://sourceforge.net/projects/gnuwin32/) ou executar diretamente os comandos docker de acordo com a necessidade.

###### build:
```bash
docker build -t $(IMAGE_NAME) .
```

###### rodar aplicação:
```bash
docker run -d -p 8080:8080 $(IMAGE_NAME)
```

*Escolha o nome que quiser para as variáveis de imagem docker e substitua "$(IMAGE_NAME)".*

***

### Execução

#### Sem Docker:
- Abra o terminal na raiz do projeto.
- Execute o comando:
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8080
    ```
- O servidor ASGI(uvicorn) executará a apicação e manterá a API no ar em http://localhost:8080.
- Você pode acessar a [documentação](http://localhost:8080/docs) e fazer requisições através da interface do Swagger ou utilizando um programa que permita criar e enviar requisições a uma API (ex.: Postman).

#### Usando Docker (recomendado):
- Abra o terminal na raiz do projeto.
- Execute o comando:
    ```bash
    make build
    ```
    Isso irá criar a imagem Docker.
- Para rodar a aplicação, execute:
    ```bash
    make run
    ```
- O servidor ASGI(uvicorn) executará a apicação e manterá a API no ar em http://localhost:8080.

### Requisições

A aplicação utiliza FastAPI, que gera uma documentação completa onde é possível visualizar todas as rotas, os modelos de objetos json para enviar nas rotas onde necessário e os erros que podem ser lançados.

#### Interface Swagger(recomendado):
- Acesse a [documentação](http://localhost:8080/docs).
- Clique na rota que deja executar.
- Clique no botão "Try it out".
- Utilize o [token](#utilizando-o-token).
- Clique no botão "Execute" para enviar a requisição e a resposta poderá ser visualizada logo abaixo na página.

#### Programas Externos:
- Com o auxílio da [documentação](http://localhost:8080/docs), crie as requisições que desejar, checando sempre a rota e o método.
- Utilize o [token](#utilizando-o-token).
- Verifique na [documentação](http://localhost:8080/docs) se é necessário enviar um body junto à requisição e o modelo json.

### Utilizando o Token

#### Interface Swagger(recomendado):
- No canto superior direito da página, clique em "Authorize".
- Preencha com o token obtido **removendo "Bearer "**.
- Clique no botão "Authorize".
*Este processo deve ser repetido sempre que um novo token for gerado para seu usuário*

- Nas requisições em que o token for requerido, preencha o campo "Authorization" com o token [obtido](#autenticando-um-usuário) (**incluindo "Bearer "**).

#### Programas Externos:
- Inclua o header Authoriation nas requisições e preencha com o token [obtido](#autenticando-um-usuário).

### Instruções

Antes de realizar qualquer requisição, autentique o seu usuário na rota de login para gerar o token que deve ser enviado nas requisições. **Sem este token, você não será capaz de acessar nenhuma rota**.

#### Credenciais:
- Existe um usuário fictício para testes:
    ```bash
    id usuário: 1 (Não é seguro expor o id assim, porém, por se tratar de uma aplicação fictícia, esse dado pode ser exigido em algumas requisições.)*
    username: moovies-api
    senha: python@MooviesApi159
    ```
- Caso deseje, você pode criar seu próprio usuário.

#### Criando um Usuário:
- Método: ```POST```
- Rota: ```/usuario```
- Body:
    ```json
    {
        "nome": "string",
        "username": "string",
        "email": "string",
        "senha": "string"
    }
    ```

#### Autenticando um Usuário:
- Método: ```POST```
- Rota: ```/login```
- Parâmetro (opcional): ```"duracao_token": int``` (Duração do token em minutos)
*(Por se tratar de uma aplicação fictícia, este parâmetro foi adicionado para que você testar e explorar o tempo de expiração do token.)*
- Body:
    ```json
    {
        "username": "string",
        "senha": "string"
    }
    ```

### Parando a Aplicação

Após utilizar a aplicação você deve pará-la.

#### Sem Docker:
- No terminal, pressione as teclas do teclado:
    ```bash
    Ctrl + C
    ```

#### Usando Docker (recomendado):
- Execute o comando:
    ```bash
    make stop
    ```

### Arquitetura

O projeto segue os princípios de **Clean Architecture** utilizando **Arquitetura em Camadas**, promovendo uma estrutura modular e flexível que separa as responsabilidades e dependências, tornando mais fácil a inteligibilidade, manutenção do código e realização de testes. A arquitetura em camadas permite fácil integração com APIs e serviços externos e facilita a implementação de novas funcionalidades e atualizações, pois cada módulo é um componente independente dentro da sua camada. Foi utilizado, ainda, o **Padrão DTO** no consumo e retorno de objetos ao cliente, permitindo melhor tratamento de dados e isolamento de atributos protegidos às camadas exeternas.
O projeto contém um sistema de autenticação simples, porém eficaz. A aplicação é capaz de gerar um token e esse token tem um prazo de validade e deve ser utilizado na demais requisições, trazendo mais segurança para a aplicação, não deixando as rotas expostas a receberem requisições de qualquer cliente não esteja.

#### Camadas

- **API**: Contém os módulos pertinentes à API, como os routers, o interceptor e o exception handler.
- **Configuração**: Contém algumas configurações necessárias para que a aplicação se comporte da maneira conforme o esperado.
- **Domain**: Contém os módulos de domínio da aplicação e componentes internos:
    - **DTOs**
    - **Models**
    - **Services**
    - **Repositories**
    - **Úteis**

#### Componentes

- **Configuração**: Responsável por abrir seções de conexão com o banco de dados e criar as estruturas de dados consumidas pela aplicação e configurações gerais do FastAPI.
- **Interceptor**: Responsável por interceptar as requisições e realizar validações de segurança e conferir permissões antes mesmo que a requisição chegue à camada responsável.
- **Router**: Responsável por processar a entrada de dados. Esse componente interage diretamente com o cliente, recebendo requisições e retornando a resposta e é a única camada acessível ao cliente.
- **Exceptions**: Responsável por cuidar e tratar das exceções lançadas pela aplicação e retornar um objeto de erro personalizado.
- **Model**: Contém as representações dos objetos de entrada e saída. Esses objetos definem as estruturas de dados utilizadas no programa.
- **Service**: Contém as regras de negócio. Esta camada encapsula a lógica central do sistema, de forma independente de tecnologias ou frameworks específicos e processa as requisições.
- **Repositório**: Responsável apenas por executar os comandos de persistência e coleta de dados através da injeção da seção aberta na classe.
- **Util**: Contém funções utilitárias compartilhadas, usadas por diferentes partes da aplicação.
- **Diretório de Testes**: Contém testes unitários e de integração para o projeto, garantindo a cobertura, a veracidade das funcionalidades e a consistência dos dados processados para todas as etapas.

#### Princípios da Arquitetura Clean Aplicados

- **Flexibilidade e Escalabilidade**: A arquitetura permite a fácil modificação e extensão do sistema, possibilitando a adição de novas funcionalidades sem comprometer a integridade da aplicação.
- **Responsabilidade Única**: Cada componente tem uma responsabilidade distinta, o que facilita o desenvolvimento e testes independentes.
- **Inversão e Injeção de Dependência**: As dependências apontam para o interior, com componentes de alto nível dependendo de componentes de baixo nível. Isso garante que a lógica de negócios esteja independente de frameworks externos.
- **Testabilidade**: A estrutura modular facilita a escrita de testes isolados para componentes individuais, promovendo o desenvolvimento orientado a testes e garantindo a confiabilidade do sistema.

#### Benefícios da Arquitetura Clean

- **Manutenibilidade**: A clara separação de responsabilidades e a definição de limites entre os componentes tornam o código mais fácil de entender e modificar.
- **Escalabilidade**: A estrutura modular permite a adição gradual de novas funcionalidades sem aumentar a complexidade do sistema.
- **Testabilidade**: A modularidade e a separação de responsabilidades facilitam testes abrangentes, ajudando a identificar bugs e regressões mais cedo.
- **Flexibilidade**: A arquitetura é adaptável a mudanças nos requisitos ou nas escolhas tecnológicas, garantindo que o sistema continue sendo viável a longo prazo.

---

## In English

### Overview

This project is the implementation of an API for a streaming platform.
The goal of this API is to allow users to make requests to rate movies and series and receive recommendations of titles to watch based on their viewing history and preferences.
This project uses a layered architecture and was developed following the principles of **Clean Architecture, SOLID, and Clean Code**, ensuring a modular, flexible, and scalable structure.

### Rules

- The API allows creating, modifying, and deleting users, as well as logging in and logging out a user;
- With the user created and logged in, an access token is generated and must be used to make further requests;
- The API can recommend movies and series to the user by performing collaborative filtering, recommending titles that other users have liked and based on content, analyzing parameters such as user ratings, genre, directors, cast, and recommending similar titles.

### Configuration

The program is developed in Python. There are two ways to configure the environment to run it:

1. **Installing Python**:
    - Go to [here](https://www.python.org/downloads/) to download Python and follow the installation instructions.
    - Open the terminal at the root of the project and install the project dependencies:
        ```bash
        pip install -r requirements.txt
        ```

2. **Using Docker (recommended)**:
    - Go to [here](https://www.docker.com/products/docker-desktop/) to download Docker and follow the installation instructions.
    - Open Docker and keep it running.
    - Use [GitBash](https://git-scm.com/downloads) to run the commands.

#### Additional Configuration

##### Windows
The project has a Dockerfile for configurations and a Makefile to execute Docker commands. If you are using a **Mac Book**, the Makefile will work correctly, and you can skip this section.

For Windows, you need to download [GNU Make for Windows](https://sourceforge.net/projects/gnuwin32/) or run the Docker commands directly as needed.


###### build:
```bash
docker build -t $(IMAGE_NAME) .
```

###### run the app:
```bash
docker run -d -p 8080:8080 $(IMAGE_NAME)
```

*You can choose whatever name you want for your docker image variables replacing "$(IMAGE_NAME)."*

***

### Execution

#### Without Docker:
- Open the terminal at the root of the project.
- Run the command:
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8080
    ```

- The ASGI server (uvicorn) will run the application and keep the API running at http://localhost:8080.
- You can access the [documentation](http://localhost:8080/docs) and make requests through the Swagger interface or using a program that allows creating and sending requests to an API (e.g., Postman).

#### Using Docker (recommended):
- Open the terminal at the root of the project.
- Run the command:
    ```bash
    make build
    ```
    This will build the Docker image.
- To run the application, execute:
    ```bash
    make run
    ```
- The ASGI server (uvicorn) will run the application and keep the API running at http://localhost:8080.

### Requests

The application uses FastAPI, which generates complete documentation where you can view all routes, JSON object models to send in the routes where necessary, and the errors that might be thrown.

#### Swagger Interface (recommended):
- Access the [documentation](http://localhost:8080/docs).
- Click on the route you want to execute.
- Click the 'Try it out' button.
- Use the [token](#using-the-token).
- Click the 'Execute' button to send the request, and the response will be displayed below the page.

#### External Programs:
- With the help of the [documentation](http://localhost:8080/docs), create the requests you want, always checking the route and the method.
- Use the [token](#using-the-token).
- Check in the [documentation](http://localhost:8080/docs) if you need to send a body with the request and the JSON model.

### Using the Token

#### Swagger Interface (recommended):
- In the top right corner of the page, click on 'Authorize'.
- Fill in with the obtained token **removing 'Bearer '**.
- Click the 'Authorize' button.
*This process should be repeated every time a new token is generated for your user.*

- For requests where the token is required, fill in the 'Authorization' field with the token [obtained](#authenticating-a-user) (**including 'Bearer '**).

#### External Programs:
- Include the 'Authorization' header in the requests and fill it with the token [obtained](#authenticating-a-user).

### Instructions

Before making any requests, authenticate your user on the login route to generate the token that must be sent in the requests. **Without this token, you will not be able to access any routes**.

#### Credentials:
- There is a dummy user for testing:
    ```bash
    user id: 1 (It is not secure to expose the id like this, but since this is a mock application, this data might be required in some requests.)*
    username: moovies-api
    password: python@MooviesApi159
    ```
- If desired, you can create your own user.

#### Creating a User:
- Method: ```POST```
- Route: ```/usuario```
- Body:
    ```json
    {
        "name": "string",
        "username": "string",
        "email": "string",
        "password": "string"
    }
    ```

#### Authenticating a User:
- Method: ```POST```
- Route: ```/login```
- Parameter (optional): ```"duracao_token": int``` (Token duration in minutes)
*(Since this is a mock application, this parameter was added for you to test and explore the token expiration time.)*
- Body:
    ```json
    {
        "username": "string",
        "password": "string"
    }
    ```

### Stopping the Application

After using the application, you should stop it.

#### Without Docker:
- In the terminal, press the following keys:
    ```bash
    Ctrl + C
    ```

#### Using Docker (recommended):
- Run the command:
    ```bash
    make stop
    ```

### Architecture

The project follows the principles of **Clean Architecture** using a **Layered Architecture**, promoting a modular and flexible structure that separates responsibilities and dependencies, making the code more understandable, maintainable, and testable. The layered architecture allows easy integration with external APIs and services and facilitates the implementation of new features and updates, as each module is an independent component within its layer. Additionally, the **DTO Pattern** was used for consuming and returning objects to the client, allowing better data handling and isolating protected attributes from external layers.
The project includes a simple yet effective authentication system. The application can generate a token, and this token has an expiration time and must be used in subsequent requests, providing more security to the application and preventing routes from being exposed to receive requests from any unauthorized client.

#### Layers

- **API**: Routers, interceptors, exception handling
- **Configuration**: General app settings and database setup
- **Domain**:
  - **DTOs**
  - **Models**
  - **Services**
  - **Repositories**
  - **Utilities**

#### Components

- **Configuration**: Responsible for opening database connection sections and creating data structures consumed by the application and general FastAPI configurations.
- **Interceptor**: Responsible for intercepting requests, performing security validations, and checking permissions before the request reaches the responsible layer.
- **Router**: Responsible for processing incoming data. This component interacts directly with the client, receiving requests and returning responses, and is the only layer accessible to the client.
- **Exceptions**: Responsible for handling and processing exceptions thrown by the application and returning a custom error object.
- **Model**: Contains representations of input and output objects. These objects define the data structures used in the program.
- **Service**: Contains business rules. This layer encapsulates the core logic of the system, independently of specific technologies or frameworks, and processes the requests.
- **Repository**: Responsible only for executing persistence commands and gathering data through the section injected in the class.
- **Util**: Contains shared utility functions used by different parts of the application.
- **Test Directory**: Contains unit and integration tests for the project, ensuring coverage, functionality accuracy, and data consistency at all stages.


---

#### Clean Architecture Principles Applied

- **Flexibility and** Scalability**: Easy to add features or change modules.
- **Single Responsibility**: Each module has a well-defined purpose.
- **Dependency Inversion**: Core logic doesn't depend on frameworks.
- **Testability**: Modules are easily testable in isolation.

#### Benefits

- **Maintainability**: Code is easier to understand and modify.
- **Scalability**: Easily extendable without increasing complexity.
- **Testability**: Supports comprehensive testing strategies.
- **Flexibility**: Adaptable to changing requirements or technologies.

---
