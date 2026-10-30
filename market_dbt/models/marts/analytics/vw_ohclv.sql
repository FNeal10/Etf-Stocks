SELECT
    ticker,
    date_key,
    open_price,
    high_price,
    low_price,
    close_price,
    volume
FROM {{ ref('stg_stocks_market_prices') }}