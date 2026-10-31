SELECT
    ticker,
    date_key,
    transaction_date,
    open_price,
    high_price,
    low_price,
    close_price,
    volume
FROM {{ ref('stg_stocks_market_prices') }}