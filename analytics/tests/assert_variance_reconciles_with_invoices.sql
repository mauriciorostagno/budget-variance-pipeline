

with mart as (
    select sum(actual_amount_usd) as total
    from {{ ref('fct_budget_variance') }}
),

fact as (
    select sum(amount_usd) as total
    from {{ ref('fct_invoices') }}
)

select
    mart.total as mart_total,
    fact.total as fact_total
from mart
cross join fact
where abs(mart.total - fact.total) > 0.01