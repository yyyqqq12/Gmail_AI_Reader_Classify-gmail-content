import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ------------------------------------------------
# EMAIL CLASSIFICATION
# ------------------------------------------------

CLASSIFY_SYSTEM = """
You classify business emails.

Return ONLY JSON.

Main categories and subcategories:

sales_documents:
- sales_quotation
- sales_order
- sales_invoice
- sales_credit_note
- sales_delivery_order

purchase_documents:
- purchase_order
- supplier_invoice
- purchase_return
- supplier_credit_note
- supplier_statement

logistics_delivery:
- goods_received_note
- shipment_notice
- parcel_tracking
- delivery_update

appointments_meetings:
- meeting_request
- meeting_confirmation
- demo_request
- calendar_invite

finance:
- bank_statement
- payment_advice
- remittance_advice

hr_internal:
- leave_request
- medical_leave
- staff_claim
- internal_memo

customer_support:
- complaint
- support_request
- warranty_claim
- technical_issue

marketing:
- promotion
- newsletter
- marketing_campaign

system_notifications:
- account_alert
- password_reset
- security_alert

uncategorized:
- needs_review

Return JSON format:

{
 "category": "...",
 "sub_category": "..."
}
"""


def classify_email(subject: str, body: str):

    prompt = f"""
Subject:
{subject}

Body:
{body}

Classify this email.
"""

    resp = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": CLASSIFY_SYSTEM},
            {"role": "user", "content": prompt},
        ],
    )

    return json.loads(resp.choices[0].message.content)


# ------------------------------------------------
# QUOTATION EXTRACTION
# ------------------------------------------------

SYSTEM_PROMPT = """
Extract quotation info from email text.

Return ONLY JSON.

Rules:
- Do not generate quotation numbers or dates
- Extract buyer information
- Extract line_items
- Use null if missing
"""

def build_prompt(raw_text: str):

    return f"""
Return JSON:

{{
 "buyer": {{
   "buyer_company_name": null,
   "buyer_name": null,
   "buyer_email": null,
   "buyer_contact": null,
   "buyer_address_line0": null
 }},
 "line_items": [
   {{
     "product_code": null,
     "item_desc": null,
     "qty": null,
     "unit_price_myr": null,
     "total_price_myr": null,
     "estimate_lead_time": null,
     "part_category": null,
     "moq_require": null
   }}
 ]
}}

Email text:
{raw_text}
"""

def extract_quotation(raw_text: str):

    resp = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_prompt(raw_text)},
        ],
    )

    return json.loads(resp.choices[0].message.content)