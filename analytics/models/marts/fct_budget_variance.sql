with budget as (
    select
        cost_center_id,
        expense_category,
        budget_month,
        sum(amount) as amount
    from {{ ref('stg_budget') }}
    group by cost_center_id, expense_category, budget_month
),

actuals as (
    select
        cost_center_key,
        expense_category,
        budget_month,
        sum(amount_usd) as amount_usd,
        sum(amount_usd) filter (where category_source = 'predicted') as amount_usd_predicted
    from {{ ref('fct_invoices') }}
    group by cost_center_key, expense_category, budget_month
),

joined as (
    select
        coalesce(b.cost_center_id, a.cost_center_key) as cost_center_key,
        coalesce(b.expense_category, a.expense_category) as expense_category,
        coalesce(b.budget_month, a.budget_month) as budget_month,
        coalesce(b.amount, 0) as budget_amount_usd, -- budget is always issued in USD
        coalesce(a.amount_usd, 0) as actual_amount_usd,
        coalesce(a.amount_usd_predicted, 0) as actual_amount_predicted_usd
    from budget b

    full outer join actuals a
        on b.cost_center_id = a.cost_center_key
        and b.expense_category = a.expense_category
        and b.budget_month = a.budget_month
)

select
    cost_center_key,
    expense_category,
    budget_month,
    budget_amount_usd,
    actual_amount_usd,
    actual_amount_predicted_usd,
    -- positive variance means actual spend exceeded the budget
    actual_amount_usd - budget_amount_usd as variance_amount_usd,
    round(
        (actual_amount_usd - budget_amount_usd) / nullif(budget_amount_usd, 0) * 100,
        2
    ) as variance_pct
from joined
