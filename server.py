"""app start"""
import pandas as pd
from sanic import Sanic, Request
from sanic.response import json as json_sanic
from sanic_ext import Extend
from mayim.extension import SanicMayimExtension
from db.executors import DailyExecutor
from tasks.daily import daily_close, get_days_of_interest

app = Sanic("Shippy")
app.add_task(daily_close)


Extend.register(
    SanicMayimExtension(
        executors=[DailyExecutor],
        dsn="postgres://postgres:3kevNFKiFNAZ@db.gwtmyrphmvdswrbssowi.supabase.co:5432/postgres",
    )
)

@app.get("/average_ohlc")
async def average_ohlc(request: Request):
    """average weekly open, close, high, low, volume for each ticker in input

    Args:
        request (Request): sanic request

    Returns:
        JSONResponse: json response of average weekly
    """
    daily_executor = DailyExecutor()
    days_of_interest = get_days_of_interest()
    tickers = request.args.get('ticker').split(',')
    results = []
    for t in tickers:
        asset = await daily_executor.select_asset(t)
        res = await daily_executor.select_ticker_closes(asset.ticker, days_of_interest[len(days_of_interest) - 1], days_of_interest[0])
        df = pd.DataFrame(res).mean()
        results.append({
            "ticker": t,
            "prices": {
                "open": round(df["open"], 1),
                "high": round(df["high"], 1),
                "low": round(df["low"], 1),
                "close": round(df["close"], 1)
            },
            "volume": int(df["volume"])
        })
    return json_sanic(results)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, auto_reload=True, workers=1)
