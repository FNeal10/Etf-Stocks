WITH daily_stock_prices AS (
    SELECT
        *
    FROM {{ source('src_daily_stock_prices', 'DAILY_STOCKS') }}
)

SELECT
    *
FROM daily_stock_prices
