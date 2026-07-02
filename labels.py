from auth import get_gmail_service

CATEGORY_LABELS = {
    "job_application": "Job Application",
    "corporate": "Corporate",
    "private": "Private"
}

_label_id_cache = {}


def get_or_create_label(service, label_name):
    if label_name in _label_id_cache:
        return _label_id_cache[label_name]
    labels = service.users().labels().list(userId="me").execute().get("labels", [])
    for label in labels:
        if label["name"] == label_name:
            _label_id_cache[label_name] = label["id"]
            return label["id"]
    new_label = service.users().labels().create(
        userId="me",
        body={
            "name": label_name,
            "labelListVisibility": "labelShow",
            "messageListVisibility": "show"
        }
    ).execute()
    _label_id_cache[label_name] = new_label["id"]
    return new_label["id"]


def apply_category_label(email_id, category, service=None):
    label_name = CATEGORY_LABELS.get(category)
    if not label_name:
        return
    if service is None:
        service = get_gmail_service()
    label_id = get_or_create_label(service, label_name)
    service.users().messages().modify(
        userId="me", id=email_id, body={"addLabelIds": [label_id]}
    ).execute()
