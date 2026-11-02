with latest_predictions as (
    select
        invoice_id,
        predicted_category,
        model_name,
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
        predictions.model_name,
        predictions.prompt_version,
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
    prompt_version,
    model_name,
    count(*) as invoices_evaluated,
    sum(is_correct) as correct_predictions,
    round(sum(is_correct) * 100.0 / count(*), 2) as accuracy_pct
from scored
group by prompt_version, model_name
order by prompt_version