import glob
import os
import uuid
from datetime import date, datetime

from db import get_connection


def load_csv_to_raw(file_path, target_table, columns, partition_column=None, partition_value=None):
    batch_id = str(uuid.uuid4())
    started_at = datetime.now()
    source_file = os.path.basename(file_path)

    conn = get_connection()
    cur = conn.cursor()

    if partition_column is None:
        cur.execute(f"truncate {target_table};")
    else:
        cur.execute(f"delete from {target_table} where {partition_column} = %s;",
                    (partition_value,),
        )

    with open(file_path, "r", encoding="utf-8") as f:
        cur.copy_expert(
            f"copy {target_table} ({columns}) "
            "from stdin with (format csv, header true)",
            f,
        )

    finished_at = datetime.now()
    row_count = cur.rowcount

    cur.execute(
        "insert into ops.ingestion_log "
        "(batch_id, target_table, source_file, started_at, finished_at, row_count, status, error_message) "
        "values (%s, %s, %s, %s, %s, %s, %s, %s)",
        (batch_id, target_table, source_file, started_at, finished_at, row_count, "success", None),
    )

    conn.commit()
    conn.close()

    print(f"{row_count} rows loaded into {target_table}")


INVOICE_COLUMNS = (
    "invoice_id, vendor_id, cost_center_id, issue_date, due_date, status, "
    "expense_category, description, amount, currency, updated_at"
)


def load_dimensions():
    load_csv_to_raw(
        "landing/vendors.csv",
        "raw.vendors",
        "vendor_id, name, vendor_type, country",
    )
    load_csv_to_raw(
        "landing/cost_centers.csv",
        "raw.cost_centers",
        "cost_center_id, name, area, owner",
    )
    load_csv_to_raw(
        "landing/budget.csv",
        "raw.budget",
        "budget_id, cost_center_id, expense_category, period_month, amount, currency",
    )
    load_csv_to_raw(
        "landing/fx_rates_2025-10-01_2026-09-30.csv",
        "raw.fx_rates",
        "rate_date, currency, units_per_usd, loaded_at",
    )


def load_all_invoice_files():
    """Load every daily invoice file sitting in landing, oldest first.

    The business date comes from the file name, so each file replaces its own
    partition and the whole folder can be reloaded without duplicating rows.
    """
    files = sorted(glob.glob("landing/invoices_*.csv"))
    for file_path in files:
        file_date = os.path.basename(file_path)[len("invoices_"):-len(".csv")]
        load_csv_to_raw(
            file_path,
            "raw.invoices",
            INVOICE_COLUMNS,
            partition_column="issue_date",
            partition_value=date.fromisoformat(file_date),
        )
    print(f"{len(files)} invoice files loaded")


if __name__ == "__main__":
    load_dimensions()
    load_all_invoice_files()
