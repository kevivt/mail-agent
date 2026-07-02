Mail Agent

A local, zero-cost AI agent that categorizes Gmail into Job Applications, Corporate, and Private, with a live dashboard and automatic Gmail label application.

Built as a portfolio project to demonstrate practical AI engineering: prompt design, evaluation, caching, and integration with a real external API — without relying on any paid service.

Why

Job-hunting means wading through a flooded inbox where actual opportunities get buried in newsletters, course notifications, and platform noise. This agent classifies incoming mail automatically and applies real Gmail labels, so the important emails are visible without manual sorting.

Stack


Python + FastAPI — backend and background sync loop
Gmail API (OAuth, gmail.modify scope) — read inbox, mark as read, apply labels
Ollama + llama3.2:3b — local LLM classification, no API costs
SQLite — caches classified emails, evicts once read
Vanilla HTML/JS — dashboard, polls every 15 seconds


How it works


A background loop polls Gmail every 5 minutes for today's unread mail.
New emails are classified by a prompted local LLM call (few-shot examples, no fine-tuning).
Classified emails are cached in SQLite and a matching Gmail label is applied.
The dashboard shows live categorized mail; "Mark all as read" writes back to Gmail directly.
Emails that become read anywhere are evicted from the cache automatically on the next sync.


Design decisions


Hand-written Python over a no-code tool (e.g. n8n) — chosen deliberately for stronger interview signal over faster setup.
Local LLM only — zero ongoing cost, and forces tighter prompt engineering since there's no larger model to fall back on.
Flat Gmail labels, not nested — the Gmail API does not reliably render /-separated label names as a nested folder structure in the sidebar, so labels are flat (Job Application, Corporate, Private) rather than prefixed.


Screenshots

(dashboard view, Gmail sidebar with applied labels)

Setup


Enable the Gmail API, create OAuth credentials, save as credentials.json in the project root.
Install Ollama and pull the model: ollama pull llama3.2:3b
pip install -r requirements.txt
python main.py
Open http://127.0.0.1:8000


First run opens a browser window for Gmail OAuth consent; a token.json is saved locally afterward.

Known limitations


Classification runs sequentially per email; not yet parallelized.
private has not fired on real inbox data — most inbound mail is automated, so this is a class-imbalance observation, not a confirmed bug.
No held-out validation yet; the 90% figure is a dev-set number, not a generalization guarantee.
