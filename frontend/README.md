# Teste Técnico - Dev. Full Stack Pleno/Sênior


# Front-end
## Arquitetura do projeto
O projeto é um simples SPA em Vue3 (Composition API) com reatividade gerenciada através de Pinia (store).

### Estrutura
```
frontend/
├── public/
├── src/
├── Dockerfile
├── index.html
├── package-lock.json
├── package.json
├── README.md
├── vite.config.js
│   

```

## Requisitos
- node 20.19.4
- Docker (para execução via container, opcional)

## Pacotes
- ``package-lock.json``
- ``package.json``


## Desenvolvimento - Modo local
Com o caminho dessa pasta ('project\frontend\') sendo exibido no terminal Windows de comando, executar:
1. ``npm run dev``

## Desenvolvimento - Docker
Com o caminho dessa pasta ('project\frontend\') sendo exibido no terminal Windows de comando, executar:
1. ``docker-compose up --build -d``
2. ``docker-compose down`` adicionar o atributo ``-v`` quando houver necessidade de remover os volumes
3. ``docker volume rm backend_postgres_data`` para remover os dados do db

## Testes - Modo local
Com o caminho dessa pasta ('project\frontend\') sendo exibido no terminal Windows de comando, executar:
