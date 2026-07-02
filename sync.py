from fetch_mails import fetch_unread_emails, get_today_unread_query
from agent import classify_email
from labels import apply_category_label
from auth import get_gmail_service
import db


def sync_inbox():
    service = get_gmail_service()  # build once, reuse for every label call this cycle

    unread_emails = fetch_unread_emails(max_results=100, query=get_today_unread_query())
    unread_ids = {e["id"] for e in unread_emails}
    cached_ids = db.get_all_cached_ids()

    read_ids = cached_ids - unread_ids
    for eid in read_ids:
        db.remove_email(eid)

    new_ids = unread_ids - cached_ids
    for e in unread_emails:
        if e["id"] in new_ids:
            category = classify_email(e["subject"], e["sender"], e["snippet"])
            e["category"] = category
            db.insert_email(e)
            apply_category_label(e["id"], category, service=service)

    return {
        "new_classified": len(new_ids),
        "removed_read": len(read_ids),
        "total_active": len(unread_ids)
    }
