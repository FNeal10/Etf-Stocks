{{
    config(
        materialized='incremental',
        unique_key='market_ticker'
    )
}}
WITH stocks_info AS (
    SELECT
        Ticker as market_ticker,
        Type as market_type,
        Name as company_name,
        Url as scraped_from
    FROM {{ ref('stg_stock_info') }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['market_ticker']) }} as market_key,
    market_ticker,
    market_type,
    company_name,
    scraped_from,
    current_timestamp() as created_at,
    current_timestamp() as updated_at
FROM stocks_info

{% if is_incremental() %}
    where market_ticker not in (select market_ticker from {{ this }})
{% endif %}

