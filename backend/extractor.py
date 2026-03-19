import json
import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

# Handle PyInstaller paths
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ENV_PATH = os.path.join(BASE_DIR, ".env")

# Load environment variables from correct path
load_dotenv(ENV_PATH)

# Debug (optional)
print("ENV PATH:", ENV_PATH)
print("API KEY FOUND:", bool(os.getenv("OPENAI_API_KEY")))

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ------------------------------------------------
# EMAIL CLASSIFICATION
# ------------------------------------------------

CLASSIFY_SYSTEM = """
You classify business emails.

Return ONLY JSON.

Main categories and subcategories:

sales_documents:
- sales_quotation (keywords: quote, quotation, price quotation, quotation for)
- sales_order (keywords: sales order, order confirmation, confirmed order)
- sales_invoice (invoice sent by our company to customer)
- supplier_invoice (invoice received from supplier)
- sales_credit_note (keywords: credit note)
- sales_delivery_order (keywords: delivery order, DO)

purchase_documents:
- purchase_order (keywords: PO, purchase order, official order)
- supplier_invoice (keywords: supplier invoice)
- purchase_return (keywords: return order)
- supplier_credit_note (keywords: supplier credit note)
- supplier_statement (keywords: account statement)

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



def classify_email(subject: str, body: str, sender: str):

    prompt = f"""
        Sender:
        {sender}

        Subject:
        {subject}

        Body:
        {body}

        Important:
        If the email sender is external (not our company),
        an "invoice" usually means supplier_invoice.

        If the email is sent by our company,
        then it is sales_invoice.

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
Extract quotation request information from email text.

Return ONLY JSON.

Rules:
- Extract buyer information from the email signature if available
- Buyer info is usually at the bottom of the email
- Look for company name, contact person, email address, phone number, address
- Extract requested products (line_items)
- If a line starts with a number, treat it as quantity
- The rest of the sentence is item_desc
- Do NOT guess missing values

Example signature:

Best regards
John Tan
ABC Engineering Sdn Bhd
john@abc.com
+60 12 345 6789

Return:

{
 "buyer":{
   "buyer_company_name":"ABC Engineering Sdn Bhd",
   "buyer_name":"John Tan",
   "buyer_email":"john@abc.com",
   "buyer_contact":"+60 12 345 6789"
 }
}
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

PO_SYSTEM_PROMPT = """
Extract purchase order information from the email.

Return ONLY JSON.

Rules:
- Extract buyer or supplier information from the email signature if available
- Look for company name, contact person, email address, phone number
- These are usually located at the bottom of the email
- Extract ordered products from the email body
- If a line starts with a number, treat it as quantity
- The rest of the sentence is item_desc
- Do not guess missing values

Important:
Supplier contact information is often in the signature.

Example signature:

Best regards
John Tan
ABC Industrial Supply
john@abc.com
+60 12 345 6789

Return:

{
 "supplier":{
   "company":"ABC Industrial Supply",
   "contact":"John Tan",
   "email":"john@abc.com",
   "phone":"+60 12 345 6789"
 }
}
"""


def build_po_prompt(raw_text: str):

    return f"""
Return JSON:

{{
  "supplier": {{
    "company": null,
    "contact": null,
    "email": null,
    "phone": null
  }},
  "line_items": [
    {{
      "product_code": null,
      "item_desc": null,
      "qty": null
    }}
  ]
}}

Email text:
{raw_text}
"""

def extract_purchase_order(raw_text: str):

    resp = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": PO_SYSTEM_PROMPT},
            {"role": "user", "content": build_po_prompt(raw_text)},
        ],
    )

    return json.loads(resp.choices[0].message.content)



# ------------------------------------------------
# INVOICE EXTRACTION
# ------------------------------------------------

INVOICE_SYSTEM_PROMPT = """
Extract invoice information from email.

Return ONLY JSON.

Rules:
- Extract buyer or customer information from email signature
- Look for company name, contact person, email address, phone
- Extract invoiced products
- Extract quantity and price if available
- Do NOT guess missing values
"""

def build_invoice_prompt(raw_text: str):

    return f"""
Return JSON:

{{
 "buyer": {{
   "buyer_company_name": null,
   "buyer_name": null,
   "buyer_email": null,
   "buyer_contact": null
 }},
 "line_items": [
  {{
    "product_code": null,
    "item_desc": null,
    "qty": null,
    "unit_price": null,
    "total_price": null
  }}
 ]
}}

Email text:
{raw_text}
"""
def extract_invoice(raw_text: str):

    resp = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": INVOICE_SYSTEM_PROMPT},
            {"role": "user", "content": build_invoice_prompt(raw_text)},
        ],
    )

    return json.loads(resp.choices[0].message.content)