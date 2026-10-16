

select
    vendor_id as vendor_key,
    vendor_name,
    vendor_type,
    country
from {{ ref('stg_vendors') }}