SELECT
    ticker,
    date_key,
    transaction_date,
    price_close,

    AVG(price_close) OVER (
        PARTITION BY ticker
        ORDER BY transaction_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS sma_7,

    AVG(price_close) OVER (
        PARTITION BY ticker
        ORDER BY transaction_date
        ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) AS sma_30,

    AVG(price_close) OVER (
        PARTITION BY ticker
        ORDER BY transaction_date
        ROWS BETWEEN 49 PRECEDING AND CURRENT ROW
    ) AS sma_50

FROM {{ ref('stg_stocks_market_prices') }}