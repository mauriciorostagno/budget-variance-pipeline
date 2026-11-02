import json
import os
import uuid
from datetime import datetime
from typing import Literal

from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel, Field

# from google import genai
from ingestion.db import get_connection

load_dotenv()

MODEL_NAME = "openai/gpt-oss-20b"
PROMPT_VERSION = "v1"
BATCH_SIZE = 50

CATEGORIES = [
    "Cloud & Software",
    "Travel",
    "Office & Supplies",
    "Marketing & Advertising",
    "Professional Services",
    "Facilities & Utilities",
    "Meals & Entertainment",
    "Shipping & Logistics",
]

class CategoryPrediction(BaseModel):
    category: Literal[
        "Cloud & Software",
        "Travel",
        "Office & Supplies",
        "Marketing & Advertising",
        "Professional Services",
        "Facilities & Utilities",
        "Meals & Entertainment",
        "Shipping & Logistics",
    ]
    confidence: float = Field(
        description="How confident you are, from 0 to 1."
    )

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def build_prompt(description):
    return f"""You are classifying corporate expense invoices for a finance team.

Assign the invoice description below to exactly one of these categories:
{", ".join(CATEGORIES)}

Rules:
- Judge only by what the description says. Do not assume anything about the company.
- If the description is vague, generic, or fits more than one category, pick the most likely one but lower your confidence.
- Use a confidence above 0.8 only when the description names something specific and unambiguous.

Invoice description: {description}
"""

def classify(description):
    prompt = build_prompt(description)

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt},
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "category_prediction",
                "schema": CategoryPrediction.model_json_schema(),
            },
        },
    )

    return CategoryPrediction.model_validate(
        json.loads(response.choices[0].message.content)
    )

def fetch_unclassified(limit):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        select invoice_id, description
        from analytics_intermediate.int_invoices_classified i
        where expense_category_raw is null
            and not exists (
                select 1
                from ml.invoice_category_predictions p
                where p.invoice_id = i.invoice_id
                    and p.prompt_version = %s
            )
        limit %s
        """,
        (PROMPT_VERSION, limit),
    )
    rows = cur.fetchall()
    conn.close()
    return rows

def save_predictions(records):
    conn = get_connection()
    cur = conn.cursor()

    cur.executemany(
        """
        insert into ml.invoice_category_predictions
            (prediction_id, invoice_id, predicted_category, model_name, prompt_version, confidence, predicted_at)
        values (%s, %s, %s, %s, %s, %s, %s)
        """,
        records,
    )
    conn.commit()
    conn.close()

def run(limit):
    rows = fetch_unclassified(limit)
    predicted_at = datetime.now()
    batch = []
    saved = 0

    for invoice_id, description in rows:
        try:
            prediction = classify(description)
        except Exception as error:
            print(f"failed on {invoice_id}: {error}")
            continue

        batch.append((
            str(uuid.uuid4()),
            invoice_id,
            prediction.category,
            MODEL_NAME,
            PROMPT_VERSION,
            prediction.confidence,
            predicted_at,
        ))

        if len(batch) >= BATCH_SIZE:
            save_predictions(batch)
            saved += len(batch)
            print(f"saved {saved} so far")
            batch = []

    if batch:
        save_predictions(batch)
        saved += len(batch)

    print(f"done: {saved} predictions saved out of {len(rows)} invoices")

if __name__ == "__main__":
    run(2000)

