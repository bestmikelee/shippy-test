
# getting started

add env variables:
- `export POLYGON_API_KEY=[YOUR-API-KEY]`
- `export POSTGRES_URL=postgres://postgres:[YOUR-PASSWORD]@db.gwtmyrphmvdswrbssowi.supabase.co:5432/postgres`

install dependencies for camelot
https://camelot-py.readthedocs.io/en/master/user/install-deps.html

`pip install -r requirements.txt`

to start server and trigger fetch market data task
`python server.py`

server is listening on port `5000`

## backfilling data:
supabase tables can be created by the sql queries in `./db/queries/create_*.sql`

pdfs should be organized under `./external/reports/[ticker]/*.pdf` ticker needs to be in uppercase

## routes:

GET `/average_ohlc`  
- params: `ticker` - tickers separated by commas  
- example `/average_ohlc?ticker=AAPL,F`
    weekends accounted for, holidays not

GET `/get_company_financials`. 
- params: `ticker` - ticker name
- params: `analyst` - `JPM | Morning`
- example `/get_company_financials?ticker=AAPL&analyst=Morning`
- requires pdfs if table is not filled already

GET `/market_cap_rank_analytics`   
    
will automatically load data into db if not found and pdf is found

daily close data will be loaded on server startup.  
rate limiting is considered and currently hardcoded into the system to 5/min

# known bugs and considerations
* duplicate rows can happen inside daily summary table since there is no logic to check for uniqueness (making it unique by date would fix the issue depending on edge case clarification)

* this was generated and all done through github codespaces.  the `.devcontainer` dir details some of the adjustments I made for this build

* alembic was left in with hopes of figuring out migrations.  - but would've taken too much time for this

* sanic was used in favor of flask because of the native async process start by sanic.  without it there, every external request would be blocking, meaning my startup script would not be initiated asynchronously and therefore block the start of the server.  this was a compromise and would be better served by separating out those responsibilities.

* sql injection is probably likely as this is the first time I'm using Mayim for a simple db orm and haven't looked at the internals of the library

