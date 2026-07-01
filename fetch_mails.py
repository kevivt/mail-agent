from auth import get_gmail_service
from datetime import datetime, timedelta


def fetch_recent_emails(max_results=20):
    service = get_gmail_service()
    results = service.users().messages().list(
        userId="me", maxResults=max_results
    ).execute()
    messages = results.get("messages", [])
    emails = []
    for msg in messages:
        msg_data = service.users().messages().get(
            userId="me", id=msg["id"], format="metadata",
            metadataHeaders=["Subject", "From"]
        ).execute()
        headers = msg_data.get("payload", {}).get("headers", [])
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "(no subject)")
        sender = next((h["value"] for h in headers if h["name"] == "From"), "(unknown sender)")
        snippet = msg_data.get("snippet", "")
        emails.append({
            "id": msg["id"],
            "subject": subject,
            "sender": sender,
            "snippet": snippet
        })
    return emails


def fetch_unread_emails(max_results=50, query="is:unread"):
    service = get_gmail_service()
    results = service.users().messages().list(
        userId="me", maxResults=max_results, q=query
    ).execute()
    messages = results.get("messages", [])
    emails = []
    for msg in messages:
        msg_data = service.users().messages().get(
            userId="me", id=msg["id"], format="metadata",
            metadataHeaders=["Subject", "From"]
        ).execute()
        headers = msg_data.get("payload", {}).get("headers", [])
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "(no subject)")
        sender = next((h["value"] for h in headers if h["name"] == "From"), "(unknown sender)")
        snippet = msg_data.get("snippet", "")
        emails.append({
            "id": msg["id"],
            "subject": subject,
            "sender": sender,
            "snippet": snippet
        })
    return emails


def get_today_unread_query():
    today = datetime.now().strftime("%Y/%m/%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y/%m/%d")
    return f"is:unread after:{today} before:{tomorrow}"


def mark_emails_as_read(email_ids):
    service = get_gmail_service()
    for eid in email_ids:
        service.users().messages().modify(
            userId="me", id=eid, body={"removeLabelIds": ["UNREAD"]}
        ).execute()


if __name__ == "__main__":
    emails = fetch_recent_emails()
    for e in emails:
        print(f"From: {e['sender']}\nSubject: {e['subject']}\nSnippet: {e['snippet']}\n---")