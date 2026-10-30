WITH monthly_prices AS (
    SELECT
        ticker,
        YEAR(transaction_date) AS year,
        MONTH(transaction_date) AS month,
        DATEFROMPARTS(
            YEAR(transaction_date),
            MONTH(transaction_date),
            1
        ) AS month_start_date,
        MIN(transaction_date) AS first_trading_date,
        MAX(transaction_date) AS last_trading_date,
        COUNT(*) AS trading_days,
        MAX(CASE
            WHEN transaction_date = first_date
            THEN close_price
        END) AS first_close,
        MAX(CASE
            WHEN transaction_date = last_date
            THEN close_price
        END) AS last_close
    FROM (
        SELECT
            ticker,
            transaction_date,
            close_price,
            MIN(transaction_date) OVER (
                PARTITION BY ticker,
                    YEAR(transaction_date),
                    MONTH(transaction_date)
            ) AS first_date,
            MAX(transaction_date) OVER (
                PARTITION BY ticker,
                    YEAR(transaction_date),
                    MONTH(transaction_date)
            ) AS last_date
        FROM {{ ref('stg_stocks_market_prices') }}
    ) AS daily
    GROUP BY
        ticker,
        YEAR(transaction_date),
        MONTH(transaction_date)
)
SELECT
    ticker,
    [year],
    [month],
    month_start_date,
    first_trading_date,
    last_trading_date,
    trading_days,
    first_close,
    last_close,
    last_close - first_close AS monthly_price_change,
    CAST(
        (last_close - first_close) * 100.0
        / NULLIF(first_close, 0)
        AS DECIMAL(18, 4)
    ) AS monthly_return_pct
FROM monthly_prices