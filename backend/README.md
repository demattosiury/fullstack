# Teste Técnico - Dev. Full Stack Pleno/Sênior


# Back-end
## Arquitetura do projeto
A arquitetura é uma variação da Clean Architecture aplicada ao FastAPI, com inspiração em princípios do Domain-Driven Design (DDD).É modular e separa bem as responsabilidades.

### Estrutura
```
backend/
├── .env
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── README.md
├── requirements.txt
├── .venv/
├── alembic/                   # Migrations
├── app/
│   ├── main.py                 # Entry point da aplicação (FastAPI)
│   ├── api/                    # Interface HTTP (camada de entrega)
│   │   ├── api_routes.py
│   │   ├── auth_routes.py
│   │   ├── gecko_routes.py
│   │   └── user_routes.py
│   ├── core/                    # Camada interna de configurações
│   │   ├── database.py
│   │   ├── logging_config.py
│   │   └── security.py
│   ├── logs/                   # Logs da api
│   │   └── api.log
│   ├── models/                 # DTOs (Data Transfer Objects) com validação
│   │   ├── gecko.py
│   │   └── user.py
│   ├── services/               # Camada de caso de uso / regras de negócio
│   │   ├── gecko_service.py
│   │   ├── indicators_service.py
│   │   └── user_service.py
│   └── tests/                  # Testes unitários

```

## Requisitos
- python 3.11.9
- Docker (para execução via container, opcional)

## Pacotes
- ``requirements.txt``


## Desenvolvimento - Modo local
Com o caminho dessa pasta ('project\backend\') sendo exibido no terminal Windows de comando, executar:
1. ``python -m venv .venv``
2. ``.\venv\Scripts\activate``
    1. Caso retorne "PSSecurityException", será necessário permitir a execução de scripts para o usuário atual com: ``Set-ExecutionPolicy RemoteSigned -Scope CurrentUser``
3. O banco de dados está junto ao ``docker-compose.yml`` no root do projeto , será necessário realizar o procedimento 'Desenvolvimento - Docker' antes do próximo passo, possibilitando a conexão com um banco de dados. Ou alterar manualmente no arquivo ``/core/database.py`` a constante ``DATABASE_URL``.
4. ``uvicorn app.main:app --reload``

## Desenvolvimento - Docker
Com o caminho dessa pasta ('project\backend\') sendo exibido no terminal Windows de comando, executar:
1. ``docker-compose up --build -d``
2. ``docker-compose down`` adicionar o atributo ``-v`` quando houver necessidade de remover os volumes
3. ``docker volume rm backend_postgres_data`` para remover os dados do db

## Alembic - Migrations no Banco de dados
É utilizado Alembic para a automatização de migrations no banco de dados.
1. Inserir Base do modelo no arquivo: ``alembic/env.py``
2. Criar migration para novo modelo: ``alembic revision --autogenerate -m "descrição da mudança"``
3. Aplicar migration no banco de dados: ``alembic upgrade head``

## Testes - Modo local
Com o caminho dessa pasta ('project\backend\') sendo exibido no terminal Windows de comando, executar:
1. ``python -m pytest``

## Documentação API

- ``http://127.0.0.1:8000/docs`` - Documentação swagger API