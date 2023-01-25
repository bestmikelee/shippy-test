"""executors for queries"""
import datetime
from mayim import PostgresExecutor, query

from db.models import Asset, Daily, Report, ShortReport


class DailyExecutor(PostgresExecutor):
    async def select_ticker_closes(
        self,
        ticker: str,
        begin_timestamp: datetime.date,
        end_timestamp: datetime.date
    ) -> list[Daily]:
        pass

    async def insert_ticker_close(
        self,
        ticker_id: int,
        close: float,
        high: float,
        low: float,
        open_p: float,
        volume: int,
        timestamp: datetime.date
    ):
        pass

    async def insert_asset(
        self,
        ticker: str,
        name: str,
        primary_exchange: str,
        market_cap: int,
        address: any,
        sic_description: str,
        total_employees: int
    ):
        pass

    @query(
        """
        SELECT *
        FROM tradeable_asset
        WHERE ticker = $ticker
        """
    )
    async def select_asset(self, ticker: str) -> Asset:
        pass

    

class ReportExecutor(PostgresExecutor):
    async def select_report(
        self,
        analyst: str,
        ticker: str
    ) -> Report:
        pass

    async def insert_report(
        self,
        ticker_id: int,
        analyst: str,
        report_year: int,
        report_path: str,
        measured_year: int,
        revenue: int,
        gross_income: int,
        ebitda: int,
        income_tax: int
    ):
        pass

    async def select_all_for_market_analysis(
        self,
        begin_timestamp: datetime.date,
        end_timestamp: datetime.date
    ) -> list[ShortReport]:
        pass