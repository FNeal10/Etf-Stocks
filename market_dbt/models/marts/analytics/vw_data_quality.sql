SELECT
    ticker,
    date_key,
    CASE
        WHEN ticker IS NULL OR LTRIM(RTRIM(ticker)) = ''
        THEN 1 ELSE 0
    END AS missing_ticker,
    CASE
        WHEN transaction_date IS NULL
        THEN 1 ELSE 0
    END AS missing_transaction_date,
    CASE
        WHEN close_price IS NULL
        THEN 1 ELSE 0
    END AS missing_close_price,
    CASE
        WHEN close_price <= 0
        THEN 1 ELSE 0
    END AS invalid_close_price,
    CASE
        WHEN high_price < low_price
        THEN 1 ELSE 0
    END AS invalid_high_low_range,
    CASE
        WHEN high_price < close_price
          OR low_price > close_price
        THEN 1 ELSE 0
    END AS close_outside_daily_range
FROM {{ ref('stg_stocks_market_prices') }}