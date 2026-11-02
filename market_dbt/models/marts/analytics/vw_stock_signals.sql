WITH signals AS (
    SELECT
        ticker,
        date_key,
        transaction_date,
        price_close,
        sma_7,
        sma_30,

        LAG(sma_7) OVER (
            PARTITION BY ticker
            ORDER BY transaction_date
        ) AS previous_sma_7,

        LAG(sma_30) OVER (
            PARTITION BY ticker
            ORDER BY transaction_date
        ) AS previous_sma_30

    FROM {{ ref('int_stock_moving_averages') }}
)

SELECT
    ticker,
    date_key,
    price_close,
    sma_7,
    sma_30,

    CASE
        WHEN previous_sma_7 <= previous_sma_30
         AND sma_7 > sma_30
            THEN 'Bullish Crossover'

        WHEN previous_sma_7 >= previous_sma_30
         AND sma_7 < sma_30
            THEN 'Bearish Crossover'

        ELSE 'No Crossover'
    END AS ma_signal

FROM signals