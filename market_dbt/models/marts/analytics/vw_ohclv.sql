SELECT
    ticker,
    date_key,
    price_open,
    price_high,
    price_low,
    price_close,
    price_volume
FROM {{ ref('stg_stocks_market_prices') }}