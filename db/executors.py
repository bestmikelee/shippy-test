"""executors for queries"""
import datetime
from mayim import PostgresExecutor, query

from db.models import Asset, Daily


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
