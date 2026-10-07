ALTER TABLE raw.invoices ADD column IF NOT EXISTS source_file text;

ALTER TABLE raw.invoices ADD column IF NOT EXISTS ingested_at timestamp;

ALTER TABLE raw.invoices ADD column IF NOT EXISTS batch_id text;

CREATE SCHEMA IF NOT EXISTS ops;

CREATE TABLE IF NOT EXISTS ops.ingestion_log (
    batch_id text primary key,
    target_table text,
    source_file text,
    started_at timestamp,
    finished_at timestamp,
    row_count integer,
    status text,
    error_message text
);