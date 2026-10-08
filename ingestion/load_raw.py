import os
import uuid
from datetime import datetime

from db import get_connection


def load_csv_to_raw(file_path, target_table, columns):
    batch_id = str(uuid.uuid4())
    started_at = datetime.now()
    source_file = os.path.basename(file_path)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(f"truncate {target_table};")

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


if __name__ == "__main__":
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
