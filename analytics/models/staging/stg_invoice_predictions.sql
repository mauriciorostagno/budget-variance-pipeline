with predictions as (

    select
        invoice_id,
        predicted_category,
        model_name,
        prompt_version,
        confidence,
        predicted_at,
        row_number() over (
            partition by invoice_id
            order by predicted_at desc, prediction_id
        ) as rn
    from {{ source('ml', 'invoice_category_predictions') }}

)

select
    invoice_id,
    predicted_category,
    model_name,
    prompt_version,
    confidence,
    predicted_at
from predictions
where rn = 1