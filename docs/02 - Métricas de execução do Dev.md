## Métricas de Execução do Desenvolvedor

Este documento apresenta as métricas de tempo de execução com base no planejamento fornecido, com foco em granularidade diária para mitigar o impacto de tarefas concomitantes.

---

### Visão Geral

O período total de trabalho registrado para o projeto **"Teste Técnico - Dev. Full Stack Pleno/Sênior"** foi de **3 dias e 18 horas e 30 minutos** (de 22/07/2025 14:00 a 26/07/2025 08:30).

---

### Análise Diária de Execução

Para evitar a distorção por tarefas concomitantes, o cálculo do tempo efetivo trabalhado por dia considera o período mínimo e máximo de atividade registrado para aquele dia.

#### Terça-feira, 22 de Julho de 2025

* **Início das Atividades:** 14:00
* **Término das Atividades:** 20:40
* **Tempo Total Ativo no Dia:** 6 horas e 40 minutos

**Tarefas Executadas:**

* **Escolher API Pública:** 10 minutos
    * Encontrar a documentação de consumo: 10 minutos
* **Desenvolver back-end:**
    * Escolher arquitetura da API: 10 minutos
    * Iniciar projeto com FastAPI (python): 10 minutos
    * Desenvolver endpoint de health check da api pública: 3 horas e 50 minutos
    * Criar teste para o endpoint de health check da api pública: 4 horas e 20 minutos
    * Desenvolver o endpoint de health check '/status': 20 minutos
    * Desenvolver o teste para o endpoint de health check '/status': 20 minutos
    * Implementar 'logger' para a api: 40 minutos

#### Quarta-feira, 23 de Julho de 2025

* **Início das Atividades:** 17:00
* **Término das Atividades:** 22:00
* **Tempo Total Ativo no Dia:** 5 horas

**Tarefas Executadas:**

* **Desenvolver back-end:**
    * Conteinerização de imagem PostgreSQL: 35 minutos
    * Conteinerização de imagem '/backend/app': 35 minutos
    * Execução 'docker-compose': 35 minutos
    * Desenvolver um módulo de conexão entre a API e o PostgreSQL: 35 minutos
    * Desenvolver 'Create and Read' usuário: 4 horas e 15 minutos
    * Desenvolver autenticação e autorização dos endpoints: 4 horas e 15 minutos
    * Desenvolver testes 'auth_routes.py': 4 horas e 15 minutos (parte 1)
    * Desenvovler testes 'security.py': 4 horas e 15 minutos
    * Desenvolver testes 'user_service.py': 4 horas e 15 minutos

#### Quinta-feira, 24 de Julho de 2025

* **Início das Atividades:** 14:00
* **Término das Atividades:** 22:20
* **Tempo Total Ativo no Dia:** 8 horas e 20 minutos

**Tarefas Executadas:**

* **Desenvolver back-end:**
    * Desenvolver testes 'auth_routes.py': 30 minutos (continuação)
    * Implementação do Alembic para automatização de migrations: 1 hora e 20 minutos
    * Ao consumir o endpoint '/importar' da API python, salvar dados de algumas moedas no banco de dados: 5 horas e 50 minutos
    * Desenvolver endpoint '/tempo-importar': 5 horas e 50 minutos

#### Sexta-feira, 25 de Julho de 2025

* **Início das Atividades:** 19:00
* **Término das Atividades:** 21:50
* **Tempo Total Ativo no Dia:** 2 horas e 50 minutos

**Tarefas Executadas:**

* **Desenvolver back-end:**
    * Desenvolver endpoint '/indicadores': 25 minutos
* **Desenvolver front-end:**
    * Escolher arquitetura da API: 5 minutos
    * Iniciar projeto com VueJs: 5 minutos
    * Criar página AuthLandingPage (login e registro): 20 minutos
    * Criar HomePage com consumo da api de forma simples: 35 minutos
    * Proteger a HomePage: 10 minutos
    * Consumir '/indicadores' da api: 30 minutos
    * Criar filtro simples na HomePage: 10 minutos
    * Conteinerização do front-end: 20 minutos

#### Sábado, 26 de Julho de 2025

* **Início das Atividades:** 01:30
* **Término das Atividades:** 07:30
* **Tempo Total Ativo no Dia:** 6 horas

**Tarefas Executadas:**

* **Desenvolver back-end:**
    * Desenvolver testes faltantes: 4 horas e 5 minutos
    * Melhorar a documentação da API: 6 horas

---

### Métricas Importantes (Tempo Líquido por Dia)

* **Tempo Total Líquido de Execução:** 28 horas e 50 minutos
    * 22/07/2025: 6 horas e 40 minutos
    * 23/07/2025: 5 horas
    * 24/07/2025: 8 horas e 20 minutos
    * 25/07/2025: 2 horas e 50 minutos
    * 26/07/2025: 6 horas
* **Tempo Médio Diário de Execução:** 5 horas e 46 minutos (28h 50min / 5 dias ativos)

---

### Observações

* As durações das tarefas individuais são calculadas como a diferença entre o início e o término, ou entre o início/continuação e término, desconsiderando pausas internas não explicitadas.
* A abordagem de "tempo total ativo no dia" serve para fornecer uma métrica mais realista da janela de trabalho, minimizando a superestimação de horas devido a tarefas concomitantes. No entanto, é importante notar que dentro dessa janela, o desenvolvedor pode ter alternado entre tarefas ou tido breves interrupções não registradas.
