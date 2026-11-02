-- Where the agent gets it wrong, and how confident it was while doing it

with latest_predictions as (

    select
        invoice_id,
        predicted_category,
        prompt_version,
        confidence,
        row_number() over (
            partition by invoice_id, prompt_version
            order by predicted_at desc
        ) as rn
    from ml.invoice_category_predictions
),

scored as (

    select
        predictions.invoice_id,
        predictions.confidence,
        predictions.predicted_category,
        ground_truth.true_category,
        case
            when predictions.predicted_category = ground_truth.true_category then 1 else 0
        end as is_correct
    from latest_predictions predictions
    inner join ml.invoice_category_ground_truth ground_truth
        on predictions.invoice_id = ground_truth.invoice_id
    where predictions.rn = 1

)

select 
    true_category,
    predicted_category,
    count(*) as errors,
    round(avg(confidence), 2) as avg_confidence
from scored
where is_correct = 0
group by true_category, predicted_category
order by errors desc