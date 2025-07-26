# Introdução: Da CoinGecko ao ICT em Criptomoedas

Este projeto marca a criação de um **Produto Mínimo Viável (MVP)** focado em explorar o potencial da **CoinGecko API** para identificar **sinais da estratégia ICT (Inner Circle Trading)** em criptomoedas. Nosso objetivo inicial foi validar a viabilidade de utilizar as **10.000 requisições mensais gratuitas** da API CoinGecko para coletar dados que pudessem alimentar análises. Com a base técnica estabelecida – incluindo a criação de uma API backend em FastAPI e uma interface frontend em Vue.js, além da conteinerização com Docker – o MVP demonstrou com sucesso a capacidade de consumir dados de mercado, armazená-los e apresentá-los de forma básica.

A próxima fase será crucial para transformar este protótipo em uma ferramenta funcional para traders, focando na integração dos princípios do ICT e na análise de múltiplos períodos gráficos (4h, 15min, 5min e 1min) para gerar sinais acionáveis.

---

## Plano de Continuidade do MVP: Rumo à Estratégia ICT

Com o MVP de consumo e apresentação de dados estabelecido, o plano de continuidade visa evoluir a solução para um produto robusto, capaz de identificar e apresentar sinais da estratégia ICT em criptomoedas.

### Fase 1: Aprofundamento da Coleta e Análise de Dados (Próximos 2-4 semanas)

1.  **Refinar Coleta de Dados da CoinGecko API:**
    * **Identificar Endpoints Específicos:** Explorar endpoints da CoinGecko que forneçam dados mais granulares e históricos, essenciais para as análises de ICT (ex: dados de OHLCV – Open, High, Low, Close, Volume – para diferentes timeframes).
    * **Otimizar Frequência de Requisições:** Desenvolver um mecanismo inteligente para gerenciar as 10.000 requisições mensais, priorizando os dados mais críticos e implementando cache para reduzir chamadas desnecessárias.
    * **Monitoramento de Limites da API:** Implementar alertas para notificar quando os limites de requisição estiverem próximos de serem atingidos, garantindo a sustentabilidade da coleta gratuita.

2.  **Desenvolvimento do Módulo de Análise ICT:**
    * **Estruturação de Dados para ICT:** Adaptar o esquema do banco de dados para armazenar os dados de OHLCV de forma eficiente, permitindo consultas rápidas para diferentes timeframes.
    * **Implementação dos Princípios ICT:** Codificar os indicadores e padrões de ICT para análise em diferentes timeframes (4h, 15min, 5min, 1min). Isso inclui:
        * **Análise de Fluxo de Ordem (Order Flow):** Detecção de blocos de ordens (Order Blocks), lacunas de valor justo (Fair Value Gaps - FVG), liquidez (Liquidity Pools).
        * **Estrutura de Mercado (Market Structure Shift - MSS):** Identificação de quebras de estrutura e mudanças de caráter.
        * **Pontos de Interesse (Points of Interest - POI):** Identificação de áreas de alta probabilidade para reversões ou continuações.
    * **Geração de Sinais:** Desenvolver lógica para combinar os indicadores e gerar sinais de entrada e saída com base na metodologia ICT (ex: confirmação no 15min, entrada no 5min/1min).

### Fase 2: Melhorias na Plataforma e Experiência do Usuário (Próximos 4-8 semanas)

1.  **Aprimoramento do Frontend:**
    * **Visualização de Sinais:** Criar componentes na interface que exibam os sinais de ICT de forma clara e intuitiva, talvez com gráficos interativos.
    * **Filtros e Alertas Personalizáveis:** Permitir que o usuário filtre os sinais por criptomoeda, timeframe ou tipo de sinal. Implementar notificações para novos sinais.
    * **Dashboard de Acompanhamento:** Desenvolver um painel onde o usuário possa visualizar as criptomoedas monitoradas e o status de seus sinais.

2.  **Robustez e Escala:**
    * **Testes Abrangentes:** Expandir a cobertura de testes (unitários, integração e end-to-end) para o módulo de análise ICT e o frontend.
    * **Otimização de Performance:** Otimizar as consultas ao banco de dados e o processamento dos sinais para garantir agilidade, especialmente com mais dados e usuários.
    * **Segurança:** Revisar e fortalecer as medidas de segurança da API e do frontend, especialmente em relação à autenticação e autorização.

### Fase 3: Validação e Iteração (Próximos 8-12 semanas)

1.  **Testes de Backtesting:** Implementar funcionalidades para testar a eficácia dos sinais ICT com dados históricos. Isso será crucial para validar a estratégia e fazer ajustes.
2.  **Feedback de Usuários:** Buscar feedback de traders para entender suas necessidades e refinar as funcionalidades do produto.
3.  **Exploração de Novas Fontes de Dados:** Se a limitação da CoinGecko API se tornar um gargalo, pesquisar e planejar a integração com outras APIs de exchanges (ex: Binance, Bybit) que ofereçam dados mais ricos ou limites maiores.
4.  **Monetização (Opcional):** Se o produto se mostrar valioso, explorar modelos de monetização, como planos premium para acesso a mais funcionalidades ou criptomoedas.
