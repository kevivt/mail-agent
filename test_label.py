"""
One-off manual test for the label auto-apply feature.
Bypasses the unread/today filter — classifies + labels the single most recent email.
Run: python test_label.py
Then check the Gmail web UI sidebar for a nested "MailAgent" > category label.
"""
from fetch_mails import fetch_recent_emails
from agent import classify_email
from labels import apply_category_label

emails = fetch_recent_emails(max_results=1)
e = emails[0]
category = classify_email(e["subject"], e["sender"], e["snippet"])
print(f"Subject: {e['subject']}")
print(f"Classified as: {category}")

apply_category_label(e["id"], category)
print("Label applied — check Gmail sidebar for MailAgent/... nesting")
