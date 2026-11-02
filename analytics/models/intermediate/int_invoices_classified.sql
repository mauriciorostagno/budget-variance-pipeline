select
    invoices.invoice_id,
    invoices.vendor_id,
    invoices.cost_center_id,
    invoices.issue_date,
    invoices.due_date,
    invoices.status,
    invoices.expense_category_raw,
    coalesce(
        invoices.expense_category_raw,
        predictions.predicted_category
    ) as expense_category,
    case
        when invoices.expense_category_raw is not null then 'reported'
        when predictions.predicted_category is not null then 'predicted'
        else 'unknown'
    end as category_source,
    predictions.confidence as prediction_confidence,
    case
        when invoices.amount < 0 then 'credit_note' else 'invoice'
    end as transaction_type,
    invoices.description,
    invoices.amount,
    invoices.currency,
    invoices.updated_at,
    coalesce(cost_centers.cost_center_id, -1) as cost_center_key
from {{ ref('stg_invoices') }} invoices
left join {{ ref('stg_cost_centers') }} cost_centers
    on invoices.cost_center_id = cost_centers.cost_center_id
left join {{ ref('stg_invoice_predictions') }} predictions
    on invoices.invoice_id = predictions.invoice_id