select
    vendor_id,
    name as vendor_name,
    vendor_type,
    country

from {{ source('raw', 'vendors') }}