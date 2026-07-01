import ollama

CATEGORIES = ["job_application", "corporate", "private"]

def classify_email(subject, sender, snippet):
    prompt = f"""Classify this email into exactly ONE category: job_application, corporate, or private.

job_application = related to job applications, interviews, recruiters, offer letters, application status
corporate = official company/business communications not related to job hunting (bills, subscriptions, work tools, notifications from services)
private = personal emails from friends, family, or individuals

Email:
From: {sender}
Subject: {subject}
Snippet: {snippet}

Respond with ONLY one word: job_application, corporate, or private. No explanation."""

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[{"role": "user", "content": prompt}]
    )

    label = response["message"]["content"].strip().lower()

    for cat in CATEGORIES:
        if cat in label:
            return cat
    return "corporate"  # fallback default

if __name__ == "__main__":
    from fetch_mails import fetch_recent_emails

    emails = fetch_recent_emails()
    for e in emails:
        category = classify_email(e["subject"], e["sender"], e["snippet"])
        print(f"[{category.upper()}] {e['subject']} — {e['sender']}")