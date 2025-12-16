{{
    config(
        matierialized='incremental',
        unique_key=['Ticker','Trade_Date']
    )
}}

with

momentum_data as (
    select
    Ticker,
    RSI_Value,
    MACD_Value,
    Signal_Line,
    Stochastic_Value,
    CCI_Value
    from {{ ref('stg_daily_stock_prices') }}

    {% if is_incremental() %}
        where Trade_Date > ( 
                select coalesce(max(Trade_Date), '1900-01-01') from {{ this }}
            )
    {% endif %}
)

select 
* 
from momentum_data