import random
import csv

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


with open("landing/vendors.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["vendor_id", "name", "vendor_type", "country"])
    
    for i in range(20):
        vendor_id = i + 1
        name = fake.company()
        vendor_type = random.choice(VENDOR_TYPES)
        country = fake.country()
        writer.writerow([vendor_id, name, vendor_type, country])

with open("landing/cost_centers.csv", "w", newline="", encoding="utf-8") as e:
    writer = csv.writer(e)
    writer.writerow(["cost_center_id", "name", "area", "owner"])

    for cost_center_id, name, area, owner in COST_CENTERS:
        writer.writerow([cost_center_id, name, area, owner])

print("vendors.csv and cost_centers.csv exported to landing/")