SELECT
    ticker,
    transaction_date,
    open_price,
    high_price,
    low_price,
    close_price,
    volume
FROM {{ ref('stg_stocks__market_prices') }}
