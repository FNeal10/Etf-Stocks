WITH performance AS (
    SELECT
        ticker,
        date_key,
        transaction_date,
        price_close,

        LAG(price_close, 7) OVER (
            PARTITION BY ticker
            ORDER BY transaction_date
        ) AS close_7d,

        LAG(price_close, 30) OVER (
            PARTITION BY ticker
            ORDER BY transaction_date
        ) AS close_30d,

        LAG(price_close, 90) OVER (
            PARTITION BY ticker
            ORDER BY transaction_date
        ) AS close_90d,

        FIRST_VALUE(price_close) OVER (
            PARTITION BY ticker, YEAR(transaction_date)
            ORDER BY transaction_date
            ROWS BETWEEN UNBOUNDED PRECEDING
            AND UNBOUNDED FOLLOWING
        ) AS year_start_close

    FROM {{ ref('stg_stocks_market_prices') }}
)

SELECT
    ticker,
    date_key,
    price_close,

    (price_close - close_7d)
        / NULLIF(close_7d, 0) * 100
        AS return_7d_pct,

    (price_close - close_30d)
        / NULLIF(close_30d, 0) * 100
        AS return_30d_pct,

    (price_close - close_90d)
        / NULLIF(close_90d, 0) * 100
        AS return_90d_pct,

    (price_close - year_start_close)
        / NULLIF(year_start_close, 0) * 100
        AS return_ytd_pct

FROM performance