# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.api import (
    api_routes,
    auth_routes,
    gecko_routes,
    user_routes,
)
from app.core.logging_config import setup_logger
from app.core.database import init_models

# Logger da aplicação
logger = logging.getLogger("app.main")
setup_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação (startup/shutdown).
    Ideal para iniciar conexões, validar dependências ou carregar modelos.
    """
    logger.info("Inicializando aplicação...")
    await init_models()
    logger.info("Aplicação pronta para receber requisições.")
    yield
    logger.info("Encerrando aplicação...")

# Instância principal do FastAPI
app = FastAPI(
    title="Teste Técnico - Dev. Full Stack Pleno/Sênior",
    description="API desenvolvida como parte do teste técnico para vaga Full Stack.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configuração de CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Use ["*"] apenas em ambientes de desenvolvimento
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro das rotas principais
app.include_router(api_routes.router, prefix="/api/v1")
app.include_router(gecko_routes.router, prefix="/api/v1")
app.include_router(auth_routes.router, prefix="/api/v1")
app.include_router(user_routes.router, prefix="/api/v1")
