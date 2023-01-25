SELECT DISTINCT
    ta.ticker,
    AVG(ta.market_cap)::numeric::bigint as avg_market_cap,
    AVG(ta.total_employees)::numeric::bigint as avg_num_employees,
    AVG(ds.volume)::numeric::bigint as avg_weekly_volume
FROM tradeable_asset ta
JOIN daily_summary ds ON ta.id = ds.ticker_id
WHERE ds.timestamp > $begin_timestamp AND ds.timestamp < $end_timestamp
GROUP BY ta.ticker
ORDER BY avg_market_cap DESC
