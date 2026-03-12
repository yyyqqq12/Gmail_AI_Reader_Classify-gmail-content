import sqlite3
import os

# Force DB to be created in same folder as this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "emails.db")

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS emails (
        id TEXT PRIMARY KEY,
        category TEXT,
        sub_category TEXT,
        subject TEXT,
        sender TEXT,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_email(email):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    try:
        cur.execute("""
        INSERT INTO emails (id, category, sub_category, subject, sender, date)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            email["id"],
            email["category"],
            email["sub_category"],
            email["subject"],
            email["sender"],
            email["date"]
        ))
    except sqlite3.IntegrityError:
        # duplicate email -> ignore
        pass

    conn.commit()
    conn.close()


def get_all_emails():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT * FROM emails")
    rows = cur.fetchall()

    conn.close()

    result = []

    for r in rows:
        result.append({
            "id": r[0],
            "category": r[1],
            "sub_category": r[2],
            "subject": r[3],
            "sender": r[4],
            "date": r[5]
        })

    return result


def clear_emails():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM emails")

    conn.commit()
    conn.close()