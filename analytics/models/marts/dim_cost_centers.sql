

select
    cost_center_id as cost_center_key,
    cost_center_name,
    area,
    owner
from {{ ref('stg_cost_centers') }}

union all

select 
    -1 as cost_center_key,
    'Unmapped (missing in source)' as cost_center_name,
    'Unmapped' as area,
    'Unmapped' as owner