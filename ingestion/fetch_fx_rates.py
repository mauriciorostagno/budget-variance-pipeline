import csv
from datetime import date, datetime

import requests

API_URL = "https://api.frankfurter.dev/v2/rates"
BASE_CURRENCY = "USD"
QUOTE_CURRENCIES = ["ARS", "EUR"]

def fetch_fx_rates(start_date, end_date):
    params = {
        "from": start_date,
        "to": end_date,
        "base": BASE_CURRENCY,
        "quotes": ",".join(QUOTE_CURRENCIES),
    }
    response = requests.get(API_URL, params=params, timeout=30)
    response.raise_for_status()
    return response.json()

def export_fx_rates(start_date, end_date):
    rates = fetch_fx_rates(start_date,end_date)
    loaded_at = datetime.now()
    file_path = f"landing/fx_rates_{start_date}_{end_date}.csv"

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["rate_date", "currency", "units_per_usd", "loaded_at"])

        for row in rates:
            writer.writerow([
                row["date"],
                row["quote"],
                row["rate"],
                loaded_at,
            ])
    print(f"{len(rates)} rates written to {file_path}")


if __name__ == "__main__":
    export_fx_rates(date(2025, 10, 1), date(2026, 9, 30))