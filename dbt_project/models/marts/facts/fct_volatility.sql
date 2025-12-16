{{
    config(
        matierialized='incremental',
        unique_key=['Ticker','Trade_Date']
    )
}}

with

volatility_data as (
    select
    Ticker,
    RSI_Value,
    Volatility_20_Day,
    BB_Middle,
    BB_Upper,
    BB_Lower,
    SAR_Value
    from {{ ref('stg_daily_stock_prices') }}

    {% if is_incremental() %}
        where Trade_Date > ( 
                select coalesce(max(Trade_Date), '1900-01-01') from {{ this }}
            )
    {% endif %}
)

select 
* from volatility_data