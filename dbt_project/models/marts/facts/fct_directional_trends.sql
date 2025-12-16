{{
    config(
        matierialized='incremental',
        unique_key=['Ticker','Trade_Date']
    )
}}

with

directional_trends_data as (
    select
    Plus_DI,
    Minus_DI,
    ADX_Value,
    from {{ ref('stg_daily_stock_prices') }}

    {% if is_incremental() %}
        where Trade_Date > ( 
                select coalesce(max(Trade_Date), '1900-01-01') from {{ this }}
            )
    {% endif %}
)

select * from
directional_trends_data