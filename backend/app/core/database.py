from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import logging
from dotenv import load_dotenv

logger = logging.getLogger("app.core.database")

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_LOCAL_URL") if os.getenv('API_ENV') == 'development' else os.getenv("DATABASE_DOCKER_URL")

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

Base = declarative_base()

# Dependency
async def get_db():
    logger.info("Iniciando sessão com banco de dados...")
    try:
        async with AsyncSessionLocal() as session:
            yield session
    except Exception as e:
        logger.error(f"Erro ao iniciar sessão com banco de dados: {e}", exc_info=True)
        raise
    finally:
        logger.info("Encerrando sessão com banco de dados.")

async def init_models():
    logger.info("Inicializando tabelas no banco de dados")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Modelos criados com sucesso")
    except Exception as e:
        logger.error(f"Erro ao criar os modelos no banco de dados: {e}", exc_info=True)
        raise
