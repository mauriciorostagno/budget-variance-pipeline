select
    budget_id,
    cost_center_id,
    expense_category,
    period_month as budget_month,
    amount,
    currency

from {{ source('raw', 'budget') }}