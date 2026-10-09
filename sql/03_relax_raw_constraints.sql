-- Raw layer keeps no uniqueness constraint on purpose.
-- Source systems do send duplicated invoice_id (re-sent files, double exports),
-- and a primary key would reject the whole COPY, losing the valid rows
-- and leaving no trace of the bad data.
-- Duplicates are detected and resolved downstream, in dbt staging.

ALTER TABLE raw.invoices
    DROP CONSTRAINT IF EXISTS invoices_pkey;