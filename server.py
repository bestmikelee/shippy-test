"""app start"""
from sanic import Sanic
from sanic.response import text
from external.polygon import get_ticker
from scripts.daily import daily_close

app = Sanic("Shippy")
app.add_task(daily_close())

@app.get("/")
async def average_ohlc(request):
    # get ticker as query params
    # execute query in service
    return text(await get_ticker(request.args.get('ticker')))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, auto_reload=True)
    
