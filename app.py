from flask import Flask, render_template

app = Flask(__name__)

@app.route("/average_ohlc")
async def average_ohlc():
    # get ticker as query params
    # execute query in service
    return "test"
