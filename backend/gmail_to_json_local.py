import os
import re
import json
import base64
from datetime import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from openpyxl import Workbook

from extractor import classify_email, extract_quotation, extract_purchase_order

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

OUTPUT_DIR = "out_json"

# ------------------------------------------------
# Gmail Auth
# ------------------------------------------------

def get_gmail_service():

    creds = None
    token_path = "token.json"

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(token_path, "w") as f:
            f.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


# ------------------------------------------------
# Decode email
# ------------------------------------------------

def _decode_b64url(data):

    raw = base64.urlsafe_b64decode(data.encode("utf-8"))
    return raw.decode("utf-8", errors="replace")


def extract_text_from_message(full_msg):

    payload = full_msg.get("payload", {})
    stack = [payload]

    best_plain = None
    best_html = None

    while stack:

        part = stack.pop()
        mime = part.get("mimeType", "")
        body = part.get("body", {})
        data = body.get("data")

        if mime == "text/plain" and data:
            best_plain = _decode_b64url(data)
            break

        if mime == "text/html" and data:
            best_html = _decode_b64url(data)

        for child in part.get("parts", []):
            stack.append(child)

    if best_plain:
        return best_plain.strip()

    if best_html:
        text = re.sub(r"<[^>]+>", " ", best_html)
        text = re.sub(r"\s+", " ", text)
        return text

    return ""


# ------------------------------------------------
# Save results
# ------------------------------------------------

def save_json_and_excel(data, filename):

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    json_path = os.path.join(OUTPUT_DIR, f"{filename}.json")

    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)

    xlsx_path = os.path.join(OUTPUT_DIR, f"{filename}.xlsx")

    wb = Workbook()
    ws = wb.active

    headers = [
        "product_code",
        "item_desc",
        "qty",
        "unit_price_myr",
        "total_price_myr",
        "estimate_lead_time",
        "part_category",
        "moq_require",
    ]

    ws.append(headers)

    for item in data.get("line_items", []):
        ws.append([item.get(h) for h in headers])

    wb.save(xlsx_path)

    print("Saved JSON:", json_path)
    print("Saved Excel:", xlsx_path)


# ------------------------------------------------
# Main
# ------------------------------------------------

def main():

    service = get_gmail_service()

    results = service.users().messages().list(
        userId="me",
        maxResults=30
    ).execute()

    msgs = results.get("messages", [])

    for m in msgs:

        msg_id = m["id"]

        full = service.users().messages().get(
            userId="me",
            id=msg_id,
            format="full"
        ).execute()

        headers = full.get("payload", {}).get("headers", [])

        subject = ""
        sender = ""

        for h in headers:

            if h["name"] == "Subject":
                subject = h["value"]

            if h["name"] == "From":
                sender = h["value"]

        raw_text = extract_text_from_message(full)

        if not raw_text:
            continue

        print("\n----------------------------")
        print("Subject:", subject)

        classification = classify_email(subject, raw_text)

        category = classification.get("category") or "others"
        sub_category = classification.get("sub_category") or "others"

        print("Category:", category)
        print("Sub:", sub_category)

        if category == "sales_documents":

            if sub_category == "sales_quotation":

                quotation_data = extract_quotation(raw_text)

                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"quotation_{ts}_{msg_id}"

                save_json_and_excel(quotation_data, filename)

            elif sub_category == "sales_order":

                order_data = extract_purchase_order(raw_text)

                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"sales_order_{ts}_{msg_id}"

                save_json_and_excel(order_data, filename)

            elif sub_category == "sales_invoice":

                invoice_data = extract_purchase_order(raw_text)

                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"invoice_{ts}_{msg_id}"

                save_json_and_excel(invoice_data, filename)

            else:

                print("Sales document but not supported yet")


if __name__ == "__main__":
    main()