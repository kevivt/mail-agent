from fastapi import FastAPI, Query
from fetch_mails import fetch_recent_emails
from agent import classify_email

app = FastAPI(title="Mail Categorization Agent")


@app.get("/")
def root():
    return {"status": "ok", "message": "Mail Categorization Agent is running"}


@app.get("/emails")
def get_classified_emails(max_results: int = Query(20, ge=1, le=100)):
    """
    Fetch recent emails from Gmail and classify each into
    job_application, corporate, or private.
    """
    emails = fetch_recent_emails(max_results=max_results)

    classified = []
    for e in emails:
        category = classify_email(e["subject"], e["sender"], e["snippet"])
        classified.append({
            "id": e["id"],
            "subject": e["subject"],
            "sender": e["sender"],
            "snippet": e["snippet"],
            "category": category
        })

    return {
        "count": len(classified),
        "emails": classified
    }