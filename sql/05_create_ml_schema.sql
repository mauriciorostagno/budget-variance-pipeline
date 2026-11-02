-- Predictions written by the invoice classification agent, not by the ingestion
-- pipeline. The agent runs between dbt staging and dbt marts: it reads invoices
-- with no reported category, asks an LLM, and lands the answer here.
--
-- One row per prediction, never one per invoice. Keeping the history is what
-- makes it possible to compare prompt versions and models against each other,
-- so the dbt model downstream picks the most recent prediction per invoice.
--
-- Confidence is the model's own estimate and is not a calibrated probability.
-- It is used only as a threshold: below it, the invoice goes to manual review.

CREATE SCHEMA IF NOT EXISTS ml;

CREATE TABLE IF NOT EXISTS ml.invoice_category_predictions (
    prediction_id text primary key,
    invoice_id  text,
    predicted_category text,
    model_name text,
    prompt_version text,
    confidence numeric(3,2),
    predicted_at timestamp
);
