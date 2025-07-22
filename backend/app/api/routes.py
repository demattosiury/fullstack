from fastapi import APIRouter
from app.services.gecko import fetch_status
from app.models.gecko import GeckoStatusResponse

router = APIRouter()

@router.get("/gecko/status", response_model=GeckoStatusResponse)
async def get_gecko_status():
    return await fetch_status()

@router.get("/status", response_model=str)
async def get_status():
    return "Ok!"

