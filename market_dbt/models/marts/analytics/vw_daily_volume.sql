SELECT
    ticker,
    date_key,
    price_volume,
    previous_volume,
    volume_change,
    volume_change_pct,
    avg_volume_30

FROM {{ ref('int_stock_volume_metrics') }}