import aiohttp

POLYGON_URL = "https://api.polygon.io"
API_KEY = "JsLCne1mbQqvUfxQgKQJ8NDytQAppHLn"

async def get_ticker(ticker):
    async with aiohttp.ClientSession() as session:
        api_url = f"{POLYGON_URL}/v3/reference/tickers/{ticker}?apiKey={API_KEY}"
        async with session.get(api_url) as response:
            return await response.text()
