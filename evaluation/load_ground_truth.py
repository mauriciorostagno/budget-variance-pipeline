import glob

from ingestion.db import get_connection

TARGET_TABLE = "ml.invoice_category_ground_truth"
COLUMNS = "invoice_id, true_category"


def load_ground_truth():
    files = sorted(glob.glob("ground_truth/invoice_categories_*.csv"))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(f"truncate {TARGET_TABLE};")

    total = 0
    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as f:
            cur.copy_expert(
                f"copy {TARGET_TABLE} ({COLUMNS}) "
                "from stdin with (format csv, header true)",
                f,
            )

        total += cur.rowcount

        cur.rowcount

    conn.commit()
    conn.close()

    print(f"{total} rows loaded from {len(files)} files")


if __name__ == "__main__":
    load_ground_truth()
