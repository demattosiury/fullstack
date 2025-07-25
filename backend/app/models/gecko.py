from sqlalchemy import Column, String, Float, Integer, BigInteger, DateTime
from app.core.database import Base
from pydantic import BaseModel

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
