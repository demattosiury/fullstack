from pydantic import BaseModel

class GeckoStatusResponse(BaseModel):
    gecko_says: str