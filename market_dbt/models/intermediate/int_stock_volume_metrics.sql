WITH volume_data AS (
    SELECT
        ticker,
        date_key,
        transaction_date,
        price_volume,

        LAG(price_volume) OVER (
            PARTITION BY ticker
            ORDER BY transaction_date
        ) AS previous_volume,

        AVG(price_volume) OVER (
            PARTITION BY ticker
            ORDER BY transaction_date
            ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
        ) AS avg_volume_30

    FROM {{ ref('stg_stocks_market_prices') }}
)

SELECT
    ticker,
    date_key,
    transaction_date,
    price_volume,
    previous_volume,
    avg_volume_30,

    price_volume - previous_volume AS volume_change,

    (price_volume - previous_volume)
        / NULLIF(previous_volume, 0) * 100
        AS volume_change_pct

FROM volume_data