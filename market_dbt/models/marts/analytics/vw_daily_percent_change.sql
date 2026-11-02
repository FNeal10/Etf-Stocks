SELECT
    ticker,
    date_key,
    price_close,
    previous_close,
    price_change,
    daily_return_pct

FROM {{ ref('int_stock_daily_returns') }}