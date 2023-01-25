import aiohttp
import json

POLYGON_URL = "https://api.polygon.io"
API_KEY = "JsLCne1mbQqvUfxQgKQJ8NDytQAppHLn"

async def get_ticker(ticker):
    async with aiohttp.ClientSession() as session:
        api_url = f"{POLYGON_URL}/v3/reference/tickers/{ticker}?apiKey={API_KEY}"
        async with session.get(api_url) as response:
            return json.loads(await response.text())['results']

async def get_ohlc(ticker: str, date: str):
    async with aiohttp.ClientSession() as session:
        api_url = f"{POLYGON_URL}/v1/open-close/{ticker}/{date}?apiKey={API_KEY}"
        print(api_url)
        async with session.get(api_url) as response:
            res = json.loads(await response.text())
            if (res['status'] == 'NOT_FOUND'):
                raise UnavailableException
            if (res.get('error') and res.get('error').find("exceeded")):
                raise RateLimitException
            print(res)
            return res

class UnavailableException(Exception):
    pass

class RateLimitException(Exception):
    pass