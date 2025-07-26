from sqlalchemy import Column, String, Float, Integer, BigInteger, DateTime
from app.core.database import Base
from pydantic import BaseModel
from datetime import datetime

class GeckoStatusResponse(BaseModel):
    gecko_says: str



class Cryptocurrency(Base):
    __tablename__ = "cryptocurrencies"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    coingecko_id = Column(String, index=True) 
    symbol = Column(String)
    name = Column(String)
    image = Column(String)
    current_price = Column(Float)
    market_cap = Column(BigInteger)
    market_cap_rank = Column(Integer)
    fully_diluted_valuation = Column(BigInteger)
    total_volume = Column(BigInteger)
    high_24h = Column(Float)
    low_24h = Column(Float)
    price_change_24h = Column(Float)
    price_change_percentage_24h = Column(Float)
    market_cap_change_24h = Column(BigInteger)
    market_cap_change_percentage_24h = Column(Float)
    circulating_supply = Column(Float)
    total_supply = Column(Float)
    max_supply = Column(Float)
    ath = Column(Float)
    ath_change_percentage = Column(Float)
    ath_date = Column(DateTime)
    atl = Column(Float)
    atl_change_percentage = Column(Float)
    atl_date = Column(DateTime)
    last_updated = Column(DateTime)
    imported_at = Column(DateTime)


class CryptocurrencySchema(BaseModel):
    id: int
    coingecko_id: str
    symbol: str
    name: str
    image: str | None = None
    current_price: float
    market_cap: int
    market_cap_rank: int
    fully_diluted_valuation: int | None = None
    total_volume: int
    high_24h: float
    low_24h: float
    price_change_24h: float
    price_change_percentage_24h: float
    market_cap_change_24h: int
    market_cap_change_percentage_24h: float
    circulating_supply: float
    total_supply: float | None = None
    max_supply: float | None = None
    ath: float
    ath_change_percentage: float
    ath_date: datetime
    atl: float
    atl_change_percentage: float
    atl_date: datetime
    last_updated: datetime
    imported_at: datetime

    model_config = {
        "from_attributes": True
    }

class CryptocurrencyIndicatorsSchema(BaseModel):
    coingecko_id: str
    name: str
    symbol: str
    percent_off_ath: float | None = None
    price_to_24h_low_ratio: float | None = None
    volume_to_market_cap_ratio: float | None = None
    days_since_ath: int | None = None
    hypothetical_total_value: float | None = None

    model_config = {
        "from_attributes": True
    }