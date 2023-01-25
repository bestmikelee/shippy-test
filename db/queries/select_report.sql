SELECT
    ir.*
FROM industry_report ir
JOIN tradeable_asset ta on ta.id = ir.ticker_id 
WHERE ta.ticker = $ticker
AND ir.analyst = $analyst