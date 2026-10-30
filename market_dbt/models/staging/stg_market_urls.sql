SELECT
    TICKER as ticker,
    [TYPE] as market_type,
    [NAME] as market_name,
    [URL] as market_url
FROM {{ source('market_urls', 'market_urls') }}