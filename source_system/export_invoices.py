from datetime import date, datetime, time, timedelta
import csv
import random

CURRENCIES = ["USD", "ARS", "EUR"]
AMOUNT_RANGES = {
    "USD": (100, 20000),
    "ARS": (150000, 25000000),
    "EUR": (100, 18000),
}
STATUSES = ["pending", "approved", "paid", "rejected"]

EXPENSE_DESCRIPTIONS = {
    "Cloud & Software": [
        "AWS monthly compute and storage",
        "Microsoft 365 licenses renewal",
        "Canva charge from card, marketing team",
        "Databricks workspace monthly",
        "HubSpot payment - CRM plan",
        "Google cloud usage, bigquery and storage",
        "Slack annual payment",
        "GitHub team licenses",
        "the usual AWS thing from this month",
        "paid the software stuff on the company card",
    ],

    "Travel": [
        "Flight tickets - client visit",
        "hotel 2 nights, Córdoba - sales visit",
        "Uber from airport to office",
        "cab from hotel to customer site",
        "rental car for Mendoza trip",
        "baggage fee on flight to Santiago",
        "train tickets + transfer for the conference",
        "hotel booking for Juan, 3 nights",
        "trip expenses from the client meeting",
        "the hotel and travel stuff from last week",
    ],

    "Office & Supplies": [
        "printer toner, the black one",
        "some A4 paper and folders from Staples",
        "new keyboard for Martín, old one stopped working",
        "USB cables + adapters for the meeting room",
        "desk chair replacement",
        "pens, notebooks and other office stuff",
        "2 monitors for the new people joining",
        "whiteboard markers and eraser",
        "bought a few things for the office, receipt attached",
        "replacement stuff for the desks",
    ],

    "Marketing & Advertising": [
        "Google ads payment for september",
        "IG campaign - hiring post boost",
        "sponsorship for the local business event",
        "flyers for next month's expo",
        "LinkedIn ads, recruitment campaign",
        "printing the banners for the stand",
        "Facebook campaign charged to company card",
        "promo material for client event",
        "paid for the ad campaign we discussed",
        "marketing expenses for the event next month",
    ],

    "Professional Services": [
        "monthly accounting fee",
        "lawyer invoice - contract review",
        "external consultant, data project",
        "tax advice for Q3 closing",
        "HR consultant work from last month",
        "audit services - advance payment",
        "freelance designer invoice",
        "legal paperwork and signatures",
        "fee for the outside guy helping us with the project",
        "professional services, invoice attached",
    ],

    "Facilities & Utilities": [
        "electricity bill for the main office",
        "internet payment - office connection",
        "water bill",
        "office cleaning for september",
        "air conditioning maintenance",
        "monthly security service",
        "office rent",
        "building expenses + common charges",
        "the usual office bills",
        "paid the rent and building charges",
    ],

    "Meals & Entertainment": [
        "lunch with client, 4 people",
        "team dinner after the workshop",
        "coffee and snacks for the meeting",
        "restaurant - Diego + customer",
        "catering for internal event",
        "pizza for the team, friday",
        "drinks after client presentation",
        "breakfast meeting at hotel",
        "lunch with the guys from ACME",
        "food for the meeting, nothing fancy",
    ],

    "Shipping & Logistics": [
        "courier to send documents to Buenos Aires",
        "DHL shipment for samples",
        "delivery of monitors to new office",
        "express shipping - contract originals",
        "local delivery, office supplies",
        "freight for event material",
        "FedEx charge from last week",
        "package sent to customer - urgent",
        "sent the documents by courier",
        "shipping cost for the stuff we sent yesterday",
    ],
}

def export_invoices(target_date):
    file_path = f"landing/invoices_{target_date}.csv"
    truth_path = f"ground_truth/invoice_categories_{target_date}.csv"
    with open(file_path, "w", newline="", encoding="utf-8") as f, \
         open(truth_path, "w", newline="", encoding="utf-8") as g:
        writer = csv.writer(f)
        truth_writer = csv.writer(g)
        writer.writerow(["invoice_id", "vendor_id", "cost_center_id", "issue_date", "due_date", "status", "expense_category", "description", "amount", "currency", "updated_at"])
        truth_writer.writerow(["invoice_id", "true_category"])
        for i in range(25):
            invoice_id = f"INV-{target_date}-{i + 1:03d}"
            vendor_id = random.randint(1, 20)
            cost_center_id =  random.randint(1, 7)
            issue_date = target_date
            due_date =  target_date + timedelta(days=30)
            status = random.choice(STATUSES)
            expense_category = random.choice(list(EXPENSE_DESCRIPTIONS))
            description = random.choice(EXPENSE_DESCRIPTIONS[expense_category])
            currency = random.choice(CURRENCIES)
            low, high = AMOUNT_RANGES[currency]
            amount = round(random.uniform(low, high), 2)
            updated_at = datetime.combine(target_date, time(random.randint(8, 18), random.randint(0, 59)))

            reported_category = expense_category
            if random.random() < 0.15:
                reported_category = None

            writer.writerow([invoice_id, vendor_id, cost_center_id, issue_date, due_date, status, reported_category, description, amount, currency, updated_at])
            truth_writer.writerow([invoice_id, expense_category])

if __name__ == "__main__":
    export_invoices(date(2026,3,14))
