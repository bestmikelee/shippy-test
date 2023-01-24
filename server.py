"""app start"""
from sanic import Sanic
from sanic.response import text
from external.polygon import get_ticker
from db.client import db
from tasks.daily import daily_close

app = Sanic("Shippy")
app.config.DB_HOST = 'db.gwtmyrphmvdswrbssowi.supabase.co'
app.config.DB_DATABASE = 'postgres'
app.config.DB_PORT = 5432
app.config.DB_USER = 'postgres'
app.config.DB_PASSWORD = 'ko%Mz&P7QCgf'
app.add_task(daily_close())
db.init_app(app)

@app.get("/average_ohlc")
async def average_ohlc(request):
    # get ticker as query params
    # execute query in service
    return text(await get_ticker(request.args.get('ticker')))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, auto_reload=False, workers=1)
