# for each ticker
# check to see if ticker information needs an update
# update/insert into db if needed
# check for daily close
# insert into db

import os
import asyncio
import json
from datetime import date, timedelta
from time import time
from mayim.exception import RecordNotFound

from db.executors import DailyExecutor
from external.polygon import RateLimitException, UnavailableException, get_ticker, get_ohlc

q = asyncio.Queue()
ONE_MINUTE = 60
LIMIT = 5

async def daily_close():
    """updates all daily close
    """
    with open(os.path.dirname(__file__) + '/stocks.txt', 'r', encoding="utf-8") as reader:
        for line in reader:
            await q.put(line.strip())
    next_minute = time() + ONE_MINUTE
    count = 0
    while not q.empty():
        ticker = await q.get()
        count = await handle_ticker(ticker, count)
        count = await handle_ohlc(ticker, count)
        if count >= LIMIT:
            sleep_time = next_minute - time()
            await asyncio.sleep(sleep_time)
            count = 0
            next_minute = next_minute + ONE_MINUTE
        q.task_done()


async def handle_ticker(ticker: str, count: int):
    executor = DailyExecutor()
    try:
        await executor.select_asset(ticker)
        # already exists
        return count
    except RecordNotFound:
        asset_full = await get_ticker(ticker)
        await executor.insert_asset(asset_full['ticker'], asset_full['name'], asset_full['primary_exchange'], asset_full['market_cap'], json.dumps(asset_full['address']), asset_full["sic_description"], asset_full["total_employees"])
    
    return count + 1

async def handle_ohlc(ticker: str, count: int):
    executor = DailyExecutor()
    asset = await executor.select_asset(ticker)
    days_of_interest = get_days_of_interest(7)
    dailies = await executor.select_ticker_closes(ticker, days_of_interest[len(days_of_interest) - 1], days_of_interest[0])
    if len(dailies) > 0:
        days_of_interest = set(days_of_interest).difference([d.timestamp for d in dailies])
    for day in days_of_interest:
        try:
            olhc = await get_ohlc(ticker, day.isoformat())
            await executor.insert_ticker_close(asset.id, olhc["close"], olhc["high"], olhc["low"], olhc["open"], olhc["volume"], olhc["from"] )
        except UnavailableException:
            pass
        except RateLimitException:
            await asyncio.sleep(ONE_MINUTE)
            count = 0
            try:
                olhc = await get_ohlc(ticker, day.isoformat())
                await executor.insert_ticker_close(asset.id, olhc["close"], olhc["high"], olhc["low"], olhc["open"], olhc["volume"], olhc["from"])
            except UnavailableException:
                pass
        count += 1
            
    return count

def get_days_of_interest(num: int = 7):
    """ ordered from today -> number of days back
    """
    today = date.today()
    day = today
    days_back = 0
    days_of_interest = []
    # starting from one day back bc same day is not yet available
    for i in range(1, num + 1):
        if day.weekday() == 0:
            days_back += 2
        day = today - timedelta(days=i+days_back);
        days_of_interest.append(day)
    return days_of_interest