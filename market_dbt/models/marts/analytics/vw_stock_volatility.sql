SELECT
    ticker,
    date_key,
    daily_return_pct,

    STDEV(daily_return_pct) OVER (
        PARTITION BY ticker
        ORDER BY transaction_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS volatility_7d,

    STDEV(daily_return_pct) OVER (
        PARTITION BY ticker
        ORDER BY transaction_date
        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) AS volatility_30d

FROM {{ ref('int_stock_daily_returns') }}