"""app start"""
import os
from dataclasses import asdict
import numpy as np
import pandas as pd
from sanic import Sanic, Request
from sanic.response import json as json_sanic
from sanic_ext import Extend
from mayim.exception import RecordNotFound
from mayim.extension import SanicMayimExtension
from db.executors import DailyExecutor, ReportExecutor
from report_parser import dataframe_to_rows, process_report
from tasks.daily import daily_close, get_days_of_interest

app = Sanic("Shippy")
app.add_task(daily_close)
POSTGRES_CONNECTION_STRING = os.getenv("POSTGRES_URL")

if POSTGRES_CONNECTION_STRING is None:
    raise Exception("need a connection string to supabase")
Extend.register(
    SanicMayimExtension(
        executors=[DailyExecutor, ReportExecutor],
        dsn=POSTGRES_CONNECTION_STRING,
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


@app.get('/get_company_financials')
async def get_company_financials(request: Request):
    ticker = request.args.get('ticker')
    analyst = request.args.get('analyst')
    report_exec = ReportExecutor()
    daily_executor = DailyExecutor()
    try:
        reports = await report_exec.select_report(analyst, ticker)
        return json_sanic([
            {
                "ticker": ticker,
                "year": r.year,
                "financials": {
                    "revenue": r.revenue,
                    "gross_income": r.gross_income,
                    "ebitda": r.ebitda,
                    "income_tax": r.income_tax
                }
            }
            for r in reports
        ])
    except RecordNotFound:
        try:
            processed = process_report(ticker, analyst)
            rows = dataframe_to_rows(processed)
            asset = await daily_executor.select_asset(ticker)
            for row in rows:
                await report_exec.insert_report(asset.id, analyst, 0, "", **row)
            return json_sanic([
                {
                    "ticker": ticker,
                    "year": r["measured_year"],
                    "financials": {
                        "revenue": r["revenue"],
                        "gross_income": r["gross_income"],
                        "ebitda": r["ebitda"],
                        "income_tax": r["income_tax"]
                    }
                }
                for r in rows
            ])
        except Exception as e:
            print(e)
    

@app.get("/market_cap_rank_analytics")
async def market_cap_rank_analytics(request: Request):
    report = {}
    report_exec = ReportExecutor()
    days = get_days_of_interest(7)
    end = days.pop()
    reports = await report_exec.select_all_for_market_analysis(end, days[0])
    df1 = pd.DataFrame(reports)
    thiry_percent_index = int(len(reports) * .3)
    splits = np.split(df1, [thiry_percent_index, len(reports) - thiry_percent_index])
    for i, s in enumerate(splits):
        cap_label = ""
        if i == 0:
            cap_label = "large_cap"
        if i == 1:
            cap_label = "mid_cap"
        if i == 2:
            cap_label = "small_cap"
        report[cap_label] = s.mean().to_dict()
    return json_sanic(report)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, auto_reload=True, workers=1)
