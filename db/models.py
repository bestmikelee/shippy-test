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

@dataclass
class Report:
    id: int
    ticker_id: int
    inserted_at: date
    updated_at: date
    analyst: str
    report_year: int
    report_path: str
    measured_year: int
    revenue: int
    gross_income: int
    ebitda: int
    income_tax: int

@dataclass
class ShortReport:
    ticker: str
    avg_market_cap: int
    avg_num_employees: int
    avg_weekly_volume: int
