WITH prices AS (
    SELECT
        ticker,
        date_key,
        transaction_date,
        price_close
    FROM {{ ref('stg_stocks_market_prices') }}
),

previous_prices AS (
    SELECT
        ticker,
        date_key,
        transaction_date,
        price_close,

        LAG(price_close) OVER (
            PARTITION BY ticker
            ORDER BY transaction_date
        ) AS previous_close

    FROM prices
)

SELECT
    ticker,
    date_key,
    transaction_date,
    price_close,
    previous_close,

    price_close - previous_close AS price_change,

    (price_close - previous_close)
        / NULLIF(previous_close, 0) * 100
        AS daily_return_pct

FROM previous_prices