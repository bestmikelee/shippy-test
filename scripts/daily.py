# for each ticker
# check to see if ticker information needs an update
# update/insert into db if needed
# check for daily close
# insert into db

import os
import asyncio
from time import time
q = asyncio.Queue()
ONE_MINUTE = 60

async def daily_close(limit=5):
    # this should be relative to current file, not executing location
    with open(os.path.dirname(__file__) + '/stocks.txt', 'r', encoding="utf-8") as reader:
        for line in reader:
            await q.put(line.strip())
    next_minute = time() + ONE_MINUTE
    cohort = 0
    while not q.empty():
        ticker = await q.get()
        print(ticker)
        print(time())
        cohort += 1
        if cohort == limit:
            sleep_time = next_minute - time()
            print(sleep_time)
            await asyncio.sleep(15)
            cohort = 0
            next_minute = next_minute + ONE_MINUTE
        q.task_done()