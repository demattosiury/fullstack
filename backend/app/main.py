from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api import gecko_routes, auth_routes, user_routes, api_routes
from app.core.logging_config import setup_logger
from app.core.database import init_models
import logging

logger = logging.getLogger("app.main")

setup_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Inicializando aplicação...")
    await init_models()
    logger.info("Aplicação pronta para receber requisições.")
    yield
    logger.info("Encerrando aplicação...")

app = FastAPI(
    title="Teste Técnico - Dev. Full Stack Pleno/Sênior Pellissari",
    lifespan=lifespan,
)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # ou use ["*"] para permitir todos (menos seguro)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_routes.router, prefix="/api/v1")
app.include_router(gecko_routes.router, prefix="/api/v1")
app.include_router(auth_routes.router, prefix="/api/v1")
app.include_router(user_routes.router, prefix="/api/v1")