
SELECT
    Ticker AS ticker,
    TransactionDate AS transaction_date,
    PriceOpen AS open_price,
    PriceHigh AS high_price,
    PriceLow AS low_price,
    PriceClose AS close_price,
    PriceVolume AS volume
FROM {{ source('market_data', 'market_prices') }}
