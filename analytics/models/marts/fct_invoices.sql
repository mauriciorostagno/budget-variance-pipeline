select
    invoices.invoice_id,
    invoices.vendor_id as vendor_key,
    invoices.cost_center_key,
    invoices.issue_date,
    invoices.due_date,
    date_trunc('month', invoices.issue_date)::date as budget_month,
    invoices.status,
    invoices.expense_category_raw,
    invoices.expense_category,
    invoices.category_source,
    invoices.prediction_confidence,
    invoices.transaction_type,
    invoices.description,
    invoices.amount,
    invoices.currency,
    invoices.amount * fx.rate_to_usd as amount_usd,
    fx.rate_to_usd,
    fx.is_rate_filled

from {{ ref('int_invoices_classified') }} invoices

left join {{ ref('int_fx_rates_daily') }} fx
    on invoices.issue_date = fx.rate_date
    and invoices.currency = fx.currency