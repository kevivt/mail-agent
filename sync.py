from fetch_mails import fetch_unread_emails, get_today_unread_query
from agent import classify_email
import db


def sync_inbox():
    unread_emails = fetch_unread_emails(max_results=100, query=get_today_unread_query())
    unread_ids = {e["id"] for e in unread_emails}
    cached_ids = db.get_all_cached_ids()

    # Emails cached before but no longer unread today => read, or day rolled over
    read_ids = cached_ids - unread_ids
    for eid in read_ids:
        db.remove_email(eid)

    # Emails unread today but not yet classified => new arrivals
    new_ids = unread_ids - cached_ids
    for e in unread_emails:
        if e["id"] in new_ids:
            category = classify_email(e["subject"], e["sender"], e["snippet"])
            e["category"] = category
            db.insert_email(e)

    return {
        "new_classified": len(new_ids),
        "removed_read": len(read_ids),
        "total_active": len(unread_ids)
    }