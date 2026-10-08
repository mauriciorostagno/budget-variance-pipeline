import uuid

from datetime import datetime
from db import get_connection

batch_id = str(uuid.uuid4())
started_at = datetime.now()

conn = get_connection()
cur = conn.cursor()

cur.execute("truncate raw.vendors;")

with open("landing/vendors.csv", "r", encoding="utf-8") as f:
    cur.copy_expert(
        "copy raw.vendors (vendor_id, name, vendor_type, country) "
        "from stdin with (format csv, header true)",
        f,
    )

finished_at = datetime.now()
row_count = cur.rowcount

cur.execute(
    "insert into ops.ingestion_log"
    "(batch_id, target_table, source_file, started_at, finished_at, row_count, status, error_message) "
    "values (%s, %s, %s, %s, %s, %s, %s, %s)",
    (batch_id, "raw.vendors", "vendors.csv", started_at, finished_at, row_count, "success", None),
)

conn.commit()
conn.close()

print("vendors and ingestion log loaded")