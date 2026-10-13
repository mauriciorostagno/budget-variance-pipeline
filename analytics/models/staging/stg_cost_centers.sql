select
    cost_center_id,
    name as cost_center_name,
    area,
    owner

from {{ source('raw', 'cost_centers') }}