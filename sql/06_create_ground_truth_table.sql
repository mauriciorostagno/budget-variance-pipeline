-- Labelled answers for measuring the classification agent.
-- The source system never sends this, so no dbt model reads it.
-- Reading it from the pipeline would be data leakage.

CREATE TABLE IF NOT EXISTS ml.invoice_category_ground_truth (
    invoice_id text primary key,
    true_category text
);