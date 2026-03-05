from database import get_all_emails
from main import ALL_CATEGORIES

emails = get_all_emails()

counts = {cat: 0 for cat in ALL_CATEGORIES}

for e in emails:
    cat = e["category"]

    if cat not in counts:
        cat = "uncategorized"

    counts[cat] += 1

print(counts)

print("Total emails:", len(get_all_emails()))