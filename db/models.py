from dataclasses import dataclass
from datetime import date
from pydantic import BaseModel

@dataclass
class Asset:
    id: int
    created_at: date
    ticker: str
    name: str
    primary_exchange: str
    market_cap: str
    address: dict
    sic_description: str
    total_employees: int

@dataclass
class Daily:
    ticker: str
    close: float
    high: float
    low: float
    open: float
    volume: int
    timestamp: date
