import asyncio
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import db
from sync import sync_inbox

app = FastAPI(title="Mail Categorization Agent")

POLL_INTERVAL_SECONDS = 300  # sync every 5 minutes; change as needed

db.init_db()


async def background_sync_loop():
    while True:
        try:
            result = sync_inbox()
            print(f"[sync] new={result['new_classified']} "
                  f"removed={result['removed_read']} "
                  f"active={result['total_active']}")
        except Exception as e:
            print(f"[sync] error: {e}")
        await asyncio.sleep(POLL_INTERVAL_SECONDS)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(background_sync_loop())


@app.get("/inbox")
def get_inbox():
    emails = db.get_all_emails()
    return {"count": len(emails), "emails": emails}


@app.get("/", response_class=HTMLResponse)
def dashboard():
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()