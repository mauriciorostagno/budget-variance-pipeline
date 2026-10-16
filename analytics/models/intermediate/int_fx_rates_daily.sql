
with date_serie as (

    select generate_series(
        (select min(rate_date) from {{ ref('stg_fx_rates') }}),
        (select max(rate_date) from {{ ref('stg_fx_rates') }}),
        interval '1 day'
    ):: date as rate_date
),
currencies as (
    select 
        distinct currency
    from {{ ref('stg_fx_rates') }}
),

all_date_currency_pairs as (
    select 
        d.rate_date,
        c.currency
    from date_serie d
    cross join currencies c
),

pairs_with_rates as (
    select
        c.rate_date,
        c.currency,
        r.rate_to_usd
    from all_date_currency_pairs c
    left join {{ ref('stg_fx_rates') }} r
        on c.rate_date = r.rate_date
        and c.currency = r.currency
),

grouped as (
    -- count() ignores nulls, so this running count only increases on days
    -- that actually have a rate. Every gap inherits the number of the last
    -- real rate, which turns each gap into a group.
    select
        rate_date,
        currency,
        rate_to_usd,
        count(rate_to_usd) over (partition by currency order by rate_date) as rate_group
    from pairs_with_rates
)

select
    rate_date,
    currency,
    first_value(rate_to_usd) over (partition by currency, rate_group order by rate_date) as rate_to_usd,
    rate_to_usd is null as is_rate_filled,
    rate_date - first_value(rate_date) over (partition by currency, rate_group order by rate_date) as days_since_last_rate
from grouped