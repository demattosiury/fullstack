# Teste Técnico - Dev. Full Stack Pleno/Sênior


# Back-end
## Arquitetura do projeto
A arquitetura é uma variação da Clean Architecture aplicada ao FastAPI, com inspiração em princípios do Domain-Driven Design (DDD).É modular e separa bem as responsabilidades.

### Estrutura
```
backend/
├── .env
├── requirements.txt
├── .venv/
├── app/
│   ├── main.py                 # Entry point da aplicação (FastAPI)
│   ├── api/                    # Interface HTTP (camada de entrega)
│   │   └── routes.py
│   ├── core/                    # Camada interna de configurações
│   │   ├── database.py
│   │   └── logging_config.py
│   ├── logs/                   # Logs da api
│   │   └── api.log
│   ├── services/               # Camada de caso de uso / regras de negócio
│   │   └── gecko.py
│   ├── models/                 # DTOs (Data Transfer Objects) com validação
│   │   └── coin.py
│   ├── tests/                  # Testes unitários

```

## Requisitos
- python 3.11.9

## Pacotes 

## Desenvolvimento - Modo local
Com o caminho dessa pasta ('project\backend\') sendo exibido no terminal Windows de comando, executar:
1. ``python -m venv .venv``
2. ``.\venv\Scripts\activate``
    1. Caso retorne "PSSecurityException", será necessário permitir a execução de scripts para o usuário atual com: ``Set-ExecutionPolicy RemoteSigned -Scope CurrentUser``
3. ``uvicorn app.main:app --reload``

## Desenvolvimento - Docker
Com o caminho dessa pasta ('project\backend\') sendo exibido no terminal Windows de comando, executar:
1. ``docker-compose up --build -d``

## Testes - Modo local
Com o caminho dessa pasta ('project\backend\') sendo exibido no terminal Windows de comando, executar:
1. ``python -m pytest``

## Documentação API

- ``http://127.0.0.1:8000/docs`` - Documentação swagger API