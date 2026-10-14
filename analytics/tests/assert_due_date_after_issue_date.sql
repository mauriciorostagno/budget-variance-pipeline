{{ config(
    severity='error',
    warn_if='>0',
    error_if='>200'
) }}

select *

from {{ ref('stg_invoices') }}

where due_date < issue_date