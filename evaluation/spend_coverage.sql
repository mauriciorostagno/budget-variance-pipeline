-- Share of spend with no category, and share classified by the agent.

select
    round(sum(actual_amount_usd)) as total_spend_usd,
    round(
        coalesce(sum(actual_amount_usd) filter (where expense_category is null), 0) * 100.0
        / sum(actual_amount_usd), 2
    ) as pct_uncategorized,
    round(
        sum(actual_amount_predicted_usd) * 100.0 / sum(actual_amount_usd), 2
    ) as pct_from_predictions
from analytics_marts.fct_budget_variance;
