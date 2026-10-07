import random
from db import get_connection

from faker import Faker

fake = Faker()

VENDOR_TYPES = ["software", "consulting", "logistics", "services", "sales"]
COST_CENTERS = [
    (1, "Marketing", "Commercial", "Laura Mendez"),
    (2, "Sales", "Commercial", "Charles Smith"),
    (3, "Accounting", "Finance", "James Ochoa"),
    (4, "Information Technology", "IT Infrastructure", "Pablo Almiron"),
    (5, "Maintenance", "Operations & Maintenance", "Luanah Clara"),
    (6, "Facilities", "Operations & Maintenance", "Sarah Boros"),
    (7, "Executive Office", "Corporate Governance", "Mike Carls"),
]

conn = get_connection()
cur = conn.cursor()

cur.execute("truncate raw.vendors, raw.cost_centers;")

for i in range(20):
    vendor_id = i + 1
    name = fake.company()
    vendor_type = random.choice(VENDOR_TYPES)
    country = fake.country()
    cur.execute(
        "insert into raw.vendors (vendor_id, name, vendor_type, country) values (%s, %s, %s, %s)",
        (vendor_id, name, vendor_type, country),
    )

for cost_center_id, name, area, owner in COST_CENTERS:
    cur.execute(
        "insert into raw.cost_centers (cost_center_id, name, area, owner) values (%s, %s, %s, %s)",
        (cost_center_id, name, area, owner),
    )

conn.commit()
conn.close()
print("20 vendors and 7 cost centers inserted")