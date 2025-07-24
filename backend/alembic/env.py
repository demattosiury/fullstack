from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
import asyncio
import os
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

# Importa DATABASE_URL e Base (com seus modelos)
from app.core.database import DATABASE_URL
from app.models.user import Base  # se tiver mais modelos, importe também

# Configuração Alembic
config = context.config
fileConfig(config.config_file_name)

# Define a URL do banco dinamicamente
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Metadados dos modelos
target_metadata = Base.metadata

# Offline mode (gera SQL mas não executa no banco)
def run_migrations_offline():
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

# Função usada dentro da conexão assíncrona
def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

# Online mode (executa no banco)
async def run_migrations_online():
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

# Executa a versão correta conforme modo (offline ou online)
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
