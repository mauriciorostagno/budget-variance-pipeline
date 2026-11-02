from datetime import date
import csv
import random

# Fixed so the generated dataset is identical on every run and machine.
random.seed(42)

from export_invoices import EXPENSE_DESCRIPTIONS

COST_CENTER_IDS = [1, 2, 3, 4, 5, 6, 7]
BUDGET_CURRENCY = "USD"

# Budgets are set once a year per cost center and category, then adjusted
# month by month. The yearly base is what makes the variance meaningful:
# without it every month would be pure noise.
BASE_RANGE = (60000, 140000)
MONTHLY_NOISE = 0.15


def month_starts(start_month, months):
    """Return the first day of each month, starting at start_month."""
    result = []
    year, month = start_month.year, start_month.month
    for _ in range(months):
        result.append(date(year, month, 1))
        month += 1
        if month > 12:
            month = 1
            year += 1
    return result


def export_budget(start_month, months, file_path="landing/budget.csv"):
    categories = list(EXPENSE_DESCRIPTIONS)
    periods = month_starts(start_month, months)

    # one yearly base per cost center and category
    base_amounts = {
        (cost_center_id, category): random.uniform(*BASE_RANGE)
        for cost_center_id in COST_CENTER_IDS
        for category in categories
    }

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "budget_id", "cost_center_id", "expense_category",
            "period_month", "amount", "currency",
        ])

        budget_id = 0
        for period_month in periods:
            for cost_center_id in COST_CENTER_IDS:
                for category in categories:
                    budget_id += 1
                    base = base_amounts[(cost_center_id, category)]
                    factor = random.uniform(1 - MONTHLY_NOISE, 1 + MONTHLY_NOISE)
                    amount = round(base * factor, 2)
                    writer.writerow([
                        budget_id, cost_center_id, category,
                        period_month, amount, BUDGET_CURRENCY,
                    ])

    print(f"{budget_id} budget rows written to {file_path}")


if __name__ == "__main__":
    export_budget(date(2025, 10, 1), 12)
