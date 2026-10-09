
with source as (
    select * from {{ source('raw','invoices') }}
),

deduplicated as (
    select
        invoice_id,
        vendor_id,
        cost_center_id,
        issue_date,
        due_date,
        status,
        expense_category,
        description,
        amount,
        currency,
        updated_at,
        row_number() over (partition by invoice_id order by updated_at desc, batch_id) as row_num
    from source
)

select 
    invoice_id,
    vendor_id,
    cost_center_id,
    issue_date,
    due_date,
    status,
    expense_category as expense_category_raw,
    description,
    amount,
    currency,
    updated_at
from deduplicated
where row_num = 1