# Teste Técnico - Dev. Full Stack Pleno/Sênior

Este projeto full stack foi desenvolvido como parte de um teste técnico no perído de 4 dias (22/07/2025 - 26/07/2025). Ele contempla tanto o **frontend** (Vue.js) quanto o **backend** (FastAPI), seguindo boas práticas como **Clean Architecture**, **DDD** e uso de **Docker** para padronizar ambientes.

> ⚠️ Desenvolvido e testado em ambiente **Windows**.

---

## Estrutura do Projeto

```
.
├── backend/         # API desenvolvida com FastAPI
├── docs/            # Documentações auxiliares (ex: Idealização, planejamento, métricas do desenvolvedor e próximos passos)
├── frontend/        # Interface web desenvolvida com Vue.js
├── docker-compose.yml
├── .gitignore
└── README.md        # Este arquivo
```

## Tecnologias Principais
- Frontend: Vue.js 3, Vite, Pinia
- Backend: FastAPI, PostgreSQL
- Containerização: Docker, Docker Compose


## Requisitos
- Node.js v20.19.4
- Python 3.11+
- Docker + Docker Compose
- Sistema operacional: Windows

## Executando o Projeto com Docker
No terminal, com o diretório raiz do projeto aberto:

- Executar os containers: ```docker-compose up --build -d```
- Parar os containers: ```docker-compose down```
- Remover volumes: ```docker-compose down -v```
- Remover banco de dados: ```docker volume rm backend_postgres_data```
- Acesse os serviços:
    - Frontend: http://localhost:5173
    - Backend: http://localhost:8000
    - Docs da API: http://localhost:8000/docs

##  Execução Manual (Desenvolvimento Local)

Existe um ``README.md`` em cada diretório da respectiva stack


## Observações

Todos os comandos foram testados em Windows Terminal.       
Ajustes podem ser necessários para sistemas Unix (Linux/macOS).     
Certifique-se de que as portas 5173, 8000 e 5432 estão livres.


