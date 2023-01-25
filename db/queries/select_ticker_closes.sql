select 
    daily_summary.close,
    daily_summary.high,
    daily_summary.low,
    daily_summary.open,
    daily_summary.volume,
    daily_summary.timestamp,
    tradeable_asset.ticker
from daily_summary
    join tradeable_asset on daily_summary.ticker_id = tradeable_asset.id
where tradeable_asset.ticker = $ticker
and daily_summary.timestamp > $begin_timestamp
and daily_summary.timestamp < $end_timestamp
order by daily_summary.timestamp desc
