with one_row_per_date as (
    select
        rate_date,
        max(loaded_at) as loaded_at
    from {{ source('raw', 'fx_rates') }}
    group by rate_date
)

select
    rate_date,
    currency,
    units_per_usd,
    1.0 / units_per_usd as rate_to_usd, -- for the conversion of each currency to usd
    loaded_at
from {{ source('raw', 'fx_rates') }}

union all

select
    rate_date,
    'USD' as currency,
    1.0 as units_per_usd,
    1.0 as rate_to_usd,
    loaded_at
from one_row_per_date
