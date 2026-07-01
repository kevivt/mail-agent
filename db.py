import sqlite3
from contextlib import contextmanager

DB_PATH = "emails.db"


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS emails (
                id TEXT PRIMARY KEY,
                subject TEXT,
                sender TEXT,
                snippet TEXT,
                category TEXT,
                classified_at TEXT
            )
        """)


def get_all_cached_ids():
    with get_conn() as conn:
        rows = conn.execute("SELECT id FROM emails").fetchall()
        return {r["id"] for r in rows}


def insert_email(email):
    with get_conn() as conn:
        conn.execute("""
            INSERT OR REPLACE INTO emails (id, subject, sender, snippet, category, classified_at)
            VALUES (?, ?, ?, ?, ?, datetime('now'))
        """, (email["id"], email["subject"], email["sender"], email["snippet"], email["category"]))


def remove_email(email_id):
    with get_conn() as conn:
        conn.execute("DELETE FROM emails WHERE id = ?", (email_id,))


def get_all_emails():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM emails ORDER BY classified_at DESC").fetchall()
        return [dict(r) for r in rows]