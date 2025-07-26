from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import logging
from dotenv import load_dotenv


# Logger específico para operações de banco de dados
logger = logging.getLogger("app.core.database")

# Carrega variáveis do arquivo .env
load_dotenv()

# Define a URL de conexão com o banco de dados com base no ambiente (desenvolvimento ou produção)
DATABASE_URL = (
    os.getenv("DATABASE_LOCAL_URL")
    if os.getenv("API_ENV") == "development"
    else os.getenv("DATABASE_DOCKER_URL")
)

# Cria engine assíncrona com SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True, future=True)


# Cria uma fábrica de sessões assíncronas
AsyncSessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# Base declarativa para os modelos do SQLAlchemy
Base = declarative_base()


# Dependency para injetar sessão de banco de dados nas rotas FastAPI
async def get_db():
    """
    Fornece uma sessão assíncrona do banco de dados para uso em rotas ou serviços.

    Esta função é usada como dependência nas rotas FastAPI e garante que:
    - A sessão seja corretamente criada e fechada.
    - Erros sejam tratados e registrados.

    Yields:
        AsyncSession: Sessão de banco de dados ativa.
    """

    logger.info("Iniciando sessão com banco de dados...")
    try:
        async with AsyncSessionLocal() as session:
            yield session
    except Exception as e:
        logger.error(f"Erro ao iniciar sessão com banco de dados: {e}", exc_info=True)
        raise
    finally:
        logger.info("Encerrando sessão com banco de dados.")


# Inicializador de modelos (tabelas) no banco de dados
async def init_models():
    """
    Cria as tabelas definidas nos modelos SQLAlchemy no banco de dados.

    Essa função deve ser chamada no início da aplicação (por exemplo, via script ou evento `startup` da FastAPI)
    para garantir que as tabelas sejam criadas com base nos modelos definidos em `Base`.

    Raises:
        Exception: Qualquer erro durante a criação das tabelas será lançado.
    """
    logger.info("Inicializando tabelas no banco de dados")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Modelos criados com sucesso")
    except Exception as e:
        logger.error(f"Erro ao criar os modelos no banco de dados: {e}", exc_info=True)
        raise
