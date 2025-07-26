## Plano de Ação: Teste Técnico - Dev. Full Stack Pleno/Sênior

Este documento descreve o plano de ação detalhado para a execução do Teste Técnico de Desenvolvedor Full Stack Pleno/Sênior. O objetivo é criar um produto mínimo viável (MVP) que consuma uma API pública (CoinGecko API) para demonstrar a capacidade de extrair, processar e apresentar dados de criptomoedas. Pretendemos explorar a viabilidade de usar o plano gratuito da CoinGecko (10.000 requisições mensais) como base para um futuro produto focado na estratégia ICT (Inner Circle Trading).

### Visão Geral do Projeto

O projeto será dividido em três grandes etapas: escolha da API pública, desenvolvimento do backend e desenvolvimento do frontend. A estimativa total para a entrega do MVP é de aproximadamente 4 dias, considerando um esforço concentrado.

### Etapas Detalhadas e Cronograma Proposto

#### 1. Escolher API Pública (Estimativa: 10 minutos)

* **Objetivo:** Selecionar uma API pública adequada para consumo, com foco em dados de criptomoedas.
* **Ações:**
    * Pesquisar e analisar APIs públicas de dados de criptomoedas que ofereçam um plano gratuito ou de baixo custo.
    * Verificar a documentação da API para entender os endpoints e limites de requisição.
* **Recursos:** Documentação da API, internet.

#### 2. Desenvolver Back-end (Estimativa: 3 dias e 16 horas)

* **Objetivo:** Construir uma API robusta em Python (FastAPI) para consumir, processar e persistir os dados da API pública, além de expor endpoints para o frontend.
* **Ações:**
    * **Escolher arquitetura da API:** Definir a estrutura do projeto e padrões de design. (10 minutos)
    * **Iniciar projeto com FastAPI (Python):** Configurar o ambiente inicial. (10 minutos)
    * **Desenvolver endpoint de health check da API pública:** Criar um endpoint para verificar a conectividade e status da API externa. (3 horas e 50 minutos)
    * **Criar teste para o endpoint de health check da API pública:** Garantir a funcionalidade do endpoint. (4 horas e 20 minutos)
    * **Desenvolver o endpoint de health check '/status':** Criar um endpoint interno para verificar o status da própria API. (20 minutos)
    * **Desenvolver o teste para o endpoint de health check '/status':** Testar a funcionalidade interna. (20 minutos)
    * **Implementar 'logger' para a API:** Configurar um sistema de log para monitoramento e depuração. (40 minutos)
    * **Conteinerização de imagem PostgreSQL:** Preparar o banco de dados para o ambiente Docker. (35 minutos)
    * **Conteinerização de imagem '/backend/app':** Criar a imagem Docker para a aplicação backend. (35 minutos)
    * **Execução 'docker-compose':** Orquestrar os contêineres do backend e banco de dados. (35 minutos)
    * **Desenvolver um módulo de conexão entre a API e o PostgreSQL:** Estabelecer a comunicação com o banco de dados. (35 minutos)
    * **Desenvolver 'Create and Read' usuário:** Implementar funcionalidades básicas de gerenciamento de usuários. (4 horas e 15 minutos)
    * **Desenvolver autenticação e autorização dos endpoints:** Proteger os endpoints da API. (4 horas e 15 minutos)
    * **Desenvolver testes 'auth\_routes.py':** Testar as rotas de autenticação. (4 horas e 45 minutos)
    * **Desenvolver testes 'security.py':** Testar as funções de segurança. (4 horas e 15 minutos)
    * **Desenvolver testes 'user\_service.py':** Testar a lógica de serviço de usuário. (4 horas e 15 minutos)
    * **Implementação do Alembic para automatização de migrations:** Gerenciar migrações de banco de dados. (1 hora e 20 minutos)
    * **Ao consumir o endpoint '/importar' da API Python, salvar dados de algumas moedas no banco de dados:** Implementar a lógica de importação de dados da CoinGecko e persistência. (5 horas e 50 minutos)
    * **Desenvolver endpoint '/tempo-importar':** Criar um endpoint para verificar o tempo de importação dos dados. (5 horas e 50 minutos)
    * **Desenvolver endpoint '/indicadores':** Criar um endpoint para expor dados processados ou indicadores. (25 minutos)
    * **Desenvolver testes faltantes:** Cobrir quaisquer lacunas de teste identificadas. (4 horas e 5 minutos)
    * **Melhorar a documentação da API:** Gerar e refinar a documentação da API (OpenAPI/Swagger). (6 horas)
* **Recursos:** Python, FastAPI, PostgreSQL, Docker, Alembic.

#### 3. Desenvolver Front-end (Estimativa: 2 horas e 50 minutos)

* **Objetivo:** Construir uma interface de usuário intuitiva usando Vue.js para interagir com o backend e visualizar os dados.
* **Ações:**
    * **Escolher arquitetura da API:** Definir a estrutura do projeto Vue.js. (5 minutos)
    * **Iniciar projeto com VueJs:** Configurar o ambiente inicial do frontend. (5 minutos)
    * **Criar página AuthLandingPage (login e registro):** Desenvolver a interface para autenticação de usuários. (20 minutos)
    * **Criar HomePage com consumo da API de forma simples:** Exibir dados básicos consumidos do backend. (35 minutos)
    * **Proteger a HomePage:** Implementar mecanismos de proteção de rota. (10 minutos)
    * **Consumir '/indicadores' da API:** Integrar o frontend com o endpoint de indicadores do backend. (30 minutos)
    * **Criar filtro simples na HomePage:** Adicionar funcionalidades básicas de filtragem de dados. (10 minutos)
    * **Conteinerização do front-end:** Criar a imagem Docker para a aplicação frontend. (20 minutos)
* **Recursos:** Vue.js, JavaScript, Docker.

### Observações Importantes

* **Concomitância de Tarefas:** Algumas tarefas podem ser iniciadas simultaneamente ou ter dependências que permitam sobreposição, como o desenvolvimento de testes em paralelo com o desenvolvimento do endpoint principal. O cronograma reflete essa possibilidade.
* **Flexibilidade:** Este plano é uma estimativa. Ajustes podem ser necessários com base nos desafios encontrados durante a execução.
* **Foco no MVP:** O objetivo é entregar um MVP funcional, priorizando as funcionalidades essenciais. Melhorias e funcionalidades adicionais serão consideradas em fases posteriores.
