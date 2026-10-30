SELECT
    ticker,
    date_key,
    close_price,
    sma_20,
    sma_50,
    rsi,
    macd,
    signal_line,
    adx,
    CASE
        WHEN sma_20 IS NULL OR sma_50 IS NULL THEN 'Insufficient Data'
        WHEN sma_20 > sma_50 THEN 'Bullish'
        WHEN sma_20 < sma_50 THEN 'Bearish'
        ELSE 'Neutral'
    END AS moving_average_signal,
    CASE
        WHEN rsi IS NULL THEN 'Insufficient Data'
        WHEN rsi >= 70 THEN 'Overbought'
        WHEN rsi <= 30 THEN 'Oversold'
        ELSE 'Neutral'
    END AS rsi_signal,
    CASE
        WHEN macd IS NULL OR signal_line IS NULL THEN 'Insufficient Data'
        WHEN macd > signal_line THEN 'Bullish'
        WHEN macd < signal_line THEN 'Bearish'
        ELSE 'Neutral'
    END AS macd_signal,
    CASE
        WHEN adx IS NULL THEN 'Insufficient Data'
        WHEN adx >= 25 THEN 'Strong Trend'
        ELSE 'Weak Trend'
    END AS trend_strength
FROM {{ ref('stg_stocks_market_prices') }}