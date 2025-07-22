from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Teste Técnico - Dev. Full Stack Pleno/Sênior Pellissari")

app.include_router(router, prefix="/api/v1")