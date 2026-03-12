from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from gmail_to_json_local import get_gmail_service, extract_text_from_message
from extractor import classify_email, extract_quotation


from database import init_db, save_email, get_all_emails
app = FastAPI()

init_db() 

ALL_CATEGORIES = {
    "sales_documents": [
        "sales_quotation",
        "sales_order",
        "sales_invoice",
        "sales_credit_note",
        "sales_delivery_order"
    ],
    "purchase_documents": [
        "purchase_order",
        "supplier_invoice",
        "purchase_return",
        "supplier_credit_note",
        "supplier_statement"
    ],
    "logistics_delivery": [
        "goods_received_note",
        "shipment_notice",
        "parcel_tracking",
        "delivery_update"
    ],
    "appointments_meetings": [
        "meeting_request",
        "meeting_confirmation",
        "demo_request",
        "calendar_invite"
    ],
    "finance": [
        "bank_statement",
        "payment_advice",
        "remittance_advice"
    ],
    "hr_internal": [
        "leave_request",
        "medical_leave",
        "staff_claim",
        "internal_memo"
    ],
    "customer_support": [
        "complaint",
        "support_request",
        "technical_issue"
    ],
    # NEW CATEGORY
    "system_notifications": [
        "security_alert",
        "account_update",
        "verification_email",
        "password_reset",
        "service_notification",
        "account_alert"
    ],
    # 👇 ADD THIS
    
    "uncategorized": [
        "unknown",
        "unclassified",
        "general",
        "needs_review"
    ]

    
}

# allow React to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------
# Fetch emails from Gmail
# ------------------------------------------------

def fetch_emails():

    service = get_gmail_service()

    results = service.users().messages().list(
        userId="me",
        maxResults=100
    ).execute()

    msgs = results.get("messages", [])

    emails = []

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
        date = ""

        for h in headers:

            if h["name"] == "Subject":
                subject = h["value"]

            if h["name"] == "From":
                sender = h["value"]

            if h["name"] == "Date":
                date = h["value"]

        raw_text = extract_text_from_message(full)

        if not raw_text:
            continue

       

        subject_lower = subject.lower()

        # ---- RULE: invoice direction ----
        if "invoice" in subject_lower:

            if "mycompany.com" not in sender.lower():
                category = "purchase_documents"
                sub_category = "supplier_invoice"

            else:
                category = "sales_documents"
                sub_category = "sales_invoice"

        else:
            classification = classify_email(subject, raw_text, sender)

            category = classification.get("category") or "uncategorized"
            sub_category = classification.get("sub_category") or "unknown"

        # detect system notifications
        if sender.lower().startswith("no-reply") or "noreply" in sender.lower():
            category = "system_notification"
            sub_category = "service_notification"

        if "security alert" in subject.lower():
            category = "system_notification"
            sub_category = "security_alert"

        # fallback
        if not category:
            category = "uncategorized"

        if not sub_category:
            sub_category = "unknown"

        emails.append({
            "category": category,
            "sub_category": sub_category,
            "subject": subject,
            "sender": sender,
            "date": date
        })

    return emails


# ------------------------------------------------
# Dashboard (category counts)
# ------------------------------------------------

@app.get("/api/email/categories")
def get_categories():

    try:

        emails = get_all_emails()

        counts = {cat: 0 for cat in ALL_CATEGORIES}

        for e in emails:

            cat = e.get("category")

            if cat in counts:
                counts[cat] += 1

        return counts

    except Exception as e:
        return {"error": str(e)}


# ------------------------------------------------
# Sub categories
# ------------------------------------------------

@app.get("/api/email/category/{category}")
def get_sub_categories(category: str):

    emails = get_all_emails()

    subs = ALL_CATEGORIES.get(category, [])

    counts = {s: 0 for s in subs}

    for e in emails:

        if e["category"] == category:

            sub = e["sub_category"]

            if sub in counts:
                counts[sub] += 1

    return counts


# ------------------------------------------------
# Email list
# ------------------------------------------------
@app.get("/api/email/category/{category}/{sub}")
def get_emails(category: str, sub: str):

    emails = get_all_emails()

    result = []

    for e in emails:
        if e["category"] == category and e["sub_category"] == sub:
            result.append(e)

    return result


@app.get("/api/load-emails")
def load_emails():

    service = get_gmail_service()

    page_token = None
    existing = {e["id"] for e in get_all_emails()}
    new_count = 0

    while True:

        results = service.users().messages().list(
            userId="me",
            maxResults=100,
            pageToken=page_token
        ).execute()

        msgs = results.get("messages", [])

        for m in msgs:

            msg_id = m["id"]

            if msg_id in existing:
                continue

            full = service.users().messages().get(
                userId="me",
                id=msg_id,
                format="full"
            ).execute()

            headers = full.get("payload", {}).get("headers", [])

            subject = ""
            sender = ""
            date = ""

            for h in headers:

                if h["name"] == "Subject":
                    subject = h["value"]

                if h["name"] == "From":
                    sender = h["value"]

                if h["name"] == "Date":
                    date = h["value"]

            raw_text = extract_text_from_message(full)

            subject_lower = subject.lower()

            # ---- RULE: invoice direction ----
            if "invoice" in subject_lower:

                if "mysoft.com" not in sender.lower():
                    category = "purchase_documents"
                    sub_category = "supplier_invoice"

                else:
                    category = "sales_documents"
                    sub_category = "sales_invoice"

            else:
                classification = classify_email(subject, raw_text, sender)

                category = classification.get("category") or "uncategorized"
                sub_category = classification.get("sub_category") or "unknown"

            email = {
                "id": msg_id,
                "category": category,
                "sub_category": sub_category,
                "subject": subject,
                "sender": sender,
                "date": date
            }

            save_email(email)

            new_count += 1

        page_token = results.get("nextPageToken")

        if not page_token:
            break

    return {
        "status": "done",
        "new_emails": new_count
    }

@app.get("/api/system/notifications")
def get_system_notifications():

    emails = get_all_emails()

    notifications = []

    for email in emails:

        # Uncategorized email warning
        if email.get("category") == "uncategorized":
            notifications.append({
                "type": "warning",
                "message": f"Uncategorized email detected: {email.get('subject')}",
                "sender": email.get("sender")
            })

        # Missing subcategory
        if email.get("sub_category") == "unknown":
            notifications.append({
                "type": "info",
                "message": f"Email missing subcategory: {email.get('subject')}",
                "sender": email.get("sender")
            })

    return notifications


@app.get("/api/email/detail/{email_id}")
def get_email_detail(email_id: str):

    service = get_gmail_service()

    full = service.users().messages().get(
        userId="me",
        id=email_id,
        format="full"
    ).execute()

    headers = full.get("payload", {}).get("headers", [])

    subject = ""
    sender = ""
    date = ""

    for h in headers:

        if h["name"] == "Subject":
            subject = h["value"]

        if h["name"] == "From":
            sender = h["value"]

        if h["name"] == "Date":
            date = h["value"]

    body = extract_text_from_message(full)

    return {
        "id": email_id,
        "subject": subject,
        "sender": sender,
        "date": date,
        "body": body
    }



@app.get("/api/create-quotation/{email_id}")
def create_quotation(email_id: str):

    service = get_gmail_service()

    full = service.users().messages().get(
        userId="me",
        id=email_id,
        format="full"
    ).execute()

    raw_text = extract_text_from_message(full)

    if not raw_text:
        return {"error": "No email body found"}

    extracted = extract_quotation(raw_text)

    return {
        "email_id": email_id,
        "quotation": extracted
    }


from extractor import extract_purchase_order

@app.get("/api/create-po/{email_id}")
def create_po(email_id: str):

    service = get_gmail_service()

    full = service.users().messages().get(
        userId="me",
        id=email_id,
        format="full"
    ).execute()

    raw_text = extract_text_from_message(full)

    if not raw_text:
        return {"error": "No email body"}

    extracted = extract_purchase_order(raw_text)

    return {
        "email_id": email_id,
        "po": extracted
    }


from extractor import extract_invoice

@app.get("/api/create-invoice/{email_id}")
def create_invoice(email_id: str):

    service = get_gmail_service()

    full = service.users().messages().get(
        userId="me",
        id=email_id,
        format="full"
    ).execute()

    raw_text = extract_text_from_message(full)

    if not raw_text:
        return {"error": "No email body"}

    extracted = extract_invoice(raw_text)

    return {
        "email_id": email_id,
        "invoice": extracted
    }


from database import clear_emails

@app.get("/api/reload-emails")
def reload_emails():

    # delete all emails first
    clear_emails()

    service = get_gmail_service()

    page_token = None
    new_count = 0

    while True:

        results = service.users().messages().list(
            userId="me",
            maxResults=100,
            pageToken=page_token
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
            date = ""

            for h in headers:

                if h["name"] == "Subject":
                    subject = h["value"]

                if h["name"] == "From":
                    sender = h["value"]

                if h["name"] == "Date":
                    date = h["value"]

            raw_text = extract_text_from_message(full)

            subject_lower = subject.lower()

            if "invoice" in subject_lower:

                if "mysoft.com" not in sender.lower():
                    category = "purchase_documents"
                    sub_category = "supplier_invoice"

                else:
                    category = "sales_documents"
                    sub_category = "sales_invoice"

            else:

                classification = classify_email(subject, raw_text, sender)

                category = classification.get("category") or "uncategorized"
                sub_category = classification.get("sub_category") or "unknown"

            email = {
                "id": msg_id,
                "category": category,
                "sub_category": sub_category,
                "subject": subject,
                "sender": sender,
                "date": date
            }

            save_email(email)

            new_count += 1

        page_token = results.get("nextPageToken")

        if not page_token:
            break

    return {
        "status": "reloaded",
        "total_emails": new_count
    }