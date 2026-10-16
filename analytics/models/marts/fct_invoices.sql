

select 
    a.invoice_id,
    a.vendor_id as vendor_key,
    a.cost_center_key,
    a.issue_date,
    a.due_date,
    date_trunc('month', a.issue_date)::date as budget_month,
    a.status,
    a.expense_category_raw,
    a.transaction_type,
    a.description,
    a.amount,
    a.currency,
    a.amount*b.rate_to_usd as amount_usd,
    b.rate_to_usd,
    b.is_rate_filled

from {{ ref('int_invoices_classified') }} a

left join {{ ref('int_fx_rates_daily') }} b
    on a.issue_date = b.rate_date
    and a.currency = b.currency