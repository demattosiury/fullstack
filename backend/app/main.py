from fastapi import FastAPI
from app.api.routes import router
from app.core.logging_config import setup_logger

setup_logger()
app = FastAPI(title="Teste Técnico - Dev. Full Stack Pleno/Sênior Pellissari")

app.include_router(router, prefix="/api/v1")