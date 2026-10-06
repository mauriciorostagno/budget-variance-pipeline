CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.vendors (
    vendor_id  integer primary key,
    name text,
    vendor_type text,
    country text
);

CREATE TABLE IF NOT EXISTS raw.cost_centers (
    cost_center_id integer primary key,
    name text,
    area text,
    owner text
);

CREATE TABLE IF NOT EXISTS raw.budget (
    budget_id integer primary key,
    cost_center_id integer,
    expense_category text,
    period_month date,
    amount numeric(14,2),
    currency text
);

CREATE TABLE IF NOT EXISTS raw.invoices (
    invoice_id text primary key,
    vendor_id integer,
    cost_center_id integer,
    issue_date date,
    due_date date,
    status text,
    expense_category text,
    description text,
    amount numeric(14,2),
    currency text,
    updated_at timestamp
);

CREATE TABLE IF NOT EXISTS raw.fx_rates (
    rate_date date,
    currency text,
    rate_to_usd numeric(18,8),
    loaded_at timestamp,
    primary key (rate_date, currency)
);
