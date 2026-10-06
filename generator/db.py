import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("PGHOST"),
        port=os.getenv("PGPORT"),
        dbname=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
    )

if __name__ == "__main__":
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("select version();")
    print(cur.fetchone())
    conn.close()
