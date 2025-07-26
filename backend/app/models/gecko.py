from sqlalchemy import Column, String, Float, Integer, BigInteger, DateTime
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

from app.core.database import Base


class GeckoStatusResponse(BaseModel):
    gecko_says: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "gecko_says": "(V3) To the Moon!",
            }
        }
    }


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
    image: Optional[str]
    current_price: float
    market_cap: int
    market_cap_rank: int
    fully_diluted_valuation: Optional[int]
    total_volume: int
    high_24h: float
    low_24h: float
    price_change_24h: float
    price_change_percentage_24h: float
    market_cap_change_24h: int
    market_cap_change_percentage_24h: float
    circulating_supply: float
    total_supply: Optional[float]
    max_supply: Optional[float]
    ath: float
    ath_change_percentage: float
    ath_date: datetime
    atl: float
    atl_change_percentage: float
    atl_date: datetime
    last_updated: datetime
    imported_at: datetime

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "coingecko_id": "bitcoin",
                "symbol": "btc",
                "name": "Bitcoin",
                "image": "https://assets.coingecko.com/coins/images/1/large/bitcoin.png",
                "current_price": 64231.12,
                "market_cap": 1250000000000,
                "market_cap_rank": 1,
                "fully_diluted_valuation": 1340000000000,
                "total_volume": 35000000000,
                "high_24h": 65000.00,
                "low_24h": 63000.00,
                "price_change_24h": -300.45,
                "price_change_percentage_24h": -0.47,
                "market_cap_change_24h": -5000000000,
                "market_cap_change_percentage_24h": -0.4,
                "circulating_supply": 19500000,
                "total_supply": 21000000,
                "max_supply": 21000000,
                "ath": 69000.00,
                "ath_change_percentage": -6.8,
                "ath_date": "2021-11-10T14:24:00Z",
                "atl": 67.81,
                "atl_change_percentage": 94400.0,
                "atl_date": "2013-07-06T00:00:00Z",
                "last_updated": "2025-07-26T12:00:00Z",
                "imported_at": "2025-07-26T12:05:00Z",
            }
        },
    }


class CryptocurrencyIndicatorsSchema(BaseModel):
    coingecko_id: str
    name: str
    symbol: str
    percent_off_ath: Optional[float]
    price_to_24h_low_ratio: Optional[float]
    volume_to_market_cap_ratio: Optional[float]
    days_since_ath: Optional[int]
    hypothetical_total_value: Optional[float]

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "coingecko_id": "bitcoin",
                "name": "Bitcoin",
                "symbol": "btc",
                "percent_off_ath": -6.8,
                "price_to_24h_low_ratio": 1.03,
                "volume_to_market_cap_ratio": 0.028,
                "days_since_ath": 987,
                "hypothetical_total_value": 123456789.0,
            }
        },
    }


class IndicatorsResponse(BaseModel):
    coins: List[CryptocurrencySchema]
    coins_indicators: List[CryptocurrencyIndicatorsSchema]

    model_config = {
        "json_schema_extra": {
            "example": {
                "coins": [
                    {
                        "id": 1,
                        "coingecko_id": "bitcoin",
                        "symbol": "btc",
                        "name": "Bitcoin",
                        "image": "https://assets.coingecko.com/coins/images/1/large/bitcoin.png",
                        "current_price": 64231.12,
                        "market_cap": 1250000000000,
                        "market_cap_rank": 1,
                        "fully_diluted_valuation": 1340000000000,
                        "total_volume": 35000000000,
                        "high_24h": 65000.00,
                        "low_24h": 63000.00,
                        "price_change_24h": -300.45,
                        "price_change_percentage_24h": -0.47,
                        "market_cap_change_24h": -5000000000,
                        "market_cap_change_percentage_24h": -0.4,
                        "circulating_supply": 19500000,
                        "total_supply": 21000000,
                        "max_supply": 21000000,
                        "ath": 69000.00,
                        "ath_change_percentage": -6.8,
                        "ath_date": "2021-11-10T14:24:00Z",
                        "atl": 67.81,
                        "atl_change_percentage": 94400.0,
                        "atl_date": "2013-07-06T00:00:00Z",
                        "last_updated": "2025-07-26T12:00:00Z",
                        "imported_at": "2025-07-26T12:05:00Z",
                    }
                ],
                "coins_indicators": [
                    {
                        "coingecko_id": "bitcoin",
                        "name": "Bitcoin",
                        "symbol": "btc",
                        "percent_off_ath": -6.8,
                        "price_to_24h_low_ratio": 1.03,
                        "volume_to_market_cap_ratio": 0.028,
                        "days_since_ath": 987,
                        "hypothetical_total_value": 123456789.0,
                    }
                ],
            }
        }
    }


class GeckoImportResponse(BaseModel):
    message: str


class GeckoWaitingTimeResponse(BaseModel):
    waiting_time: int
    can_import: bool
