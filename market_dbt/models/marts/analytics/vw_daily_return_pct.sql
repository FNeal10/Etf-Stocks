WITH prices AS (
    SELECT
        ticker,
        date_key,
        transaction_date,
        close_price
    FROM {{ ref('stg_stocks_market_prices') }}
),

previous_prices AS (
    SELECT
        ticker,
        date_key,
        close_price,
        lag(close_price) OVER(PARTITION BY ticker ORDER BY transaction_date) AS previous_close
        FROM prices
)
SELECT
    ticker,
    date_key,
    close_price,
    close_price - previous_close AS price_change,
    CAST
    (
        (close_price - previous_close) / previous_close * 100 AS DECIMAL(10,2)
    ) AS daily_return_pct
FROM previous_prices


