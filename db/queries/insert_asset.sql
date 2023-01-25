insert into tradeable_asset (
    ticker,
    name,
    primary_exchange,
    market_cap,
    address,
    sic_description,
    total_employees
) values (
    $ticker,
    $name,
    $primary_exchange,
    $market_cap,
    $address,
    $sic_description,
    $total_employees
)