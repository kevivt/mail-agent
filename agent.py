
import ollama

CATEGORIES = ["job_application", "corporate", "private"]

def classify_email(subject, sender, snippet):
    prompt = f"""Classify this email into exactly ONE category: job_application, corporate, or private.

job_application = ANY email about a real job/internship opportunity for YOU: job alerts, postings, recruiter outreach, shortlisting, interview invites, application status, hiring events/hackathons you could apply to. Emails from PESU placements <pesuplacements@pes.edu> about internships, full-time roles, or career opportunities are ALWAYS job_application, even if forwarded ("Fwd:") or addressed to a whole batch.

corporate = official company/business communications NOT about a job opportunity for you: personalized automated updates from apps/platforms (e.g. "Vivek, your update is ready" from daily.dev), notifications about OTHER people's jobs/careers, product/feature announcements even from platforms like LinkedIn, online courses, subscriptions, bills, service notifications, marketing, and non-job requests.

private = personal emails from an actual individual human (friend, family, colleague writing to you directly) — NOT an automated service, even if it uses your first name.

Examples:
- "Your connection Tejas just started a new job!" from LinkedIn → corporate (it's about Tejas, not a job opportunity for you)
- "A grade required for capstone teammate" from Reddit → corporate (student project request, not a job opportunity)
- "Ready: Neural Networks and Deep Learning course" from Coursera → corporate (online course notification, not a job opportunity)
- "Code with Cisco | Shortlist" from campus placements → job_application (you've been shortlisted for a hiring process)
- "Myntra HIRING Hackathon 2026" from campus placements → job_application (a hiring event you could apply to)
- "Student Intern - MEI at General Motors" from LinkedIn Job Alerts → job_application (a job posting relevant to you)
- "Vivek, your personal update from daily.dev is ready" from daily.dev → corporate (automated app notification using your name, not a real person)
- "Bringing speed and strong cost performance..." from Google Cloud via LinkedIn → corporate (product announcement, not a job opportunity)

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