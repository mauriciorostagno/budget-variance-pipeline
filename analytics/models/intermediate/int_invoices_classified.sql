select 
    invoices.invoice_id,
    invoices.vendor_id,
    invoices.cost_center_id,
    invoices.issue_date,
    invoices.due_date,
    invoices.status,
    invoices.expense_category_raw,
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