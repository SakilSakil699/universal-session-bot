
"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

Standalone dashboard server.
Run alongside bot: python -m api.dashboard
"""
import asyncio
import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from config import settings, Author, BOT_VERSION, BOT_NAME
from db import db, crud
from utils import get_logger

log = get_logger("api.dashboard")


# ═══════════════════════════════════════════════
#  WebSocket Manager
# ═══════════════════════════════════════════════

class WSManager:
    """Track live WebSocket clients."""

    def __init__(self):
        self.clients: set[WebSocket] = set()

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.clients.add(ws)
        log.info(f"WS client connected. Total: {len(self.clients)}")

    def disconnect(self, ws: WebSocket):
        self.clients.discard(ws)
        log.info(f"WS client disconnected. Total: {len(self.clients)}")

    async def broadcast(self, data: dict):
        dead = []
        for ws in self.clients:
            try:
                await ws.send_json(data)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(ws)


ws_manager = WSManager()


# ═══════════════════════════════════════════════
#  Lifespan
# ═══════════════════════════════════════════════

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown."""
    log.info(f"🚀 {BOT_NAME} Dashboard starting...")
    try:
        await db.init()
        log.info("✅ Database connected")
    except Exception as e:
        log.warning(f"⚠️  DB init failed: {e}")

    # Background stats pusher
    task = asyncio.create_task(stats_pusher())

    yield

    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass
    await db.close()
    log.info("🛑 Dashboard stopped")


async def stats_pusher():
    """Push live stats to all WS clients every 5s."""
    while True:
        try:
            if ws_manager.clients:
                async with db.session() as s:
                    stats = await crud.get_stats(s)
                await ws_manager.broadcast({
                    "type": "stats",
                    "data": stats,
                })
        except Exception as e:
            log.error(f"Stats push error: {e}")
        await asyncio.sleep(5)


# ═══════════════════════════════════════════════
#  App
# ═══════════════════════════════════════════════

app = FastAPI(
    title=f"{BOT_NAME} Dashboard",
    version=BOT_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ═══════════════════════════════════════════════
#  HTML Dashboard
# ═══════════════════════════════════════════════

DASHBOARD_HTML = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{BOT_NAME} · Dashboard</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: #0a0e27;
    color: #e0e6ff;
    min-height: 100vh;
    padding: 24px;
  }}
  .header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 32px;
    padding-bottom: 20px;
    border-bottom: 1px solid rgba(124,156,255,0.15);
  }}
  h1 {{
    font-size: 1.8rem;
    background: linear-gradient(135deg, #7c9cff, #b48cff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }}
  .status {{
    display: flex;
    align-items: center;
    gap: 8px;
    color: #6ee7b7;
    font-size: 0.9rem;
  }}
  .dot {{
    width: 8px; height: 8px;
    background: #6ee7b7;
    border-radius: 50%;
    animation: pulse 2s infinite;
  }}
  @keyframes pulse {{
    0%,100% {{ opacity:1; }}
    50% {{ opacity:0.4; }}
  }}
  .grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 16px;
    margin-bottom: 32px;
  }}
  .card {{
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(124,156,255,0.15);
    border-radius: 12px;
    padding: 24px;
    transition: all 0.2s;
  }}
  .card:hover {{
    border-color: rgba(124,156,255,0.4);
    transform: translateY(-2px);
  }}
  .card .label {{
    font-size: 0.85rem;
    color: #8892b0;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 12px;
  }}
  .card .value {{
    font-size: 2.2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #7c9cff, #b48cff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }}
  .card .icon {{
    font-size: 1.4rem;
    margin-bottom: 8px;
  }}
  .footer {{
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid rgba(124,156,255,0.15);
    text-align: center;
    color: #8892b0;
    font-size: 0.9rem;
  }}
  .footer a {{
    color: #7c9cff;
    text-decoration: none;
  }}
  .footer a:hover {{ text-decoration: underline; }}
</style>
</head>
<body>
  <div class="header">
    <h1>🔐 {BOT_NAME}</h1>
    <div class="status">
      <div class="dot"></div>
      <span id="status-text">Connecting...</span>
    </div>
  </div>

  <div class="grid">
    <div class="card">
      <div class="icon">👥</div>
      <div class="label">Total Users</div>
      <div class="value" id="total-users">—</div>
    </div>
    <div class="card">
      <div class="icon">⚡</div>
      <div class="label">Active Today</div>
      <div class="value" id="active-today">—</div>
    </div>
    <div class="card">
      <div class="icon">🔐</div>
      <div class="label">Total Sessions</div>
      <div class="value" id="total-sessions">—</div>
    </div>
    <div class="card">
      <div class="icon">📊</div>
      <div class="label">Sessions Today</div>
      <div class="value" id="sessions-today">—</div>
    </div>
  </div>

  <div class="footer">
    Made with ❤️  by
    <a href="{Author.TELEGRAM_URL}" target="_blank">{Author.NAME}</a>
    · <a href="{Author.GITHUB_URL}" target="_blank">GitHub</a>
    · <span style="color:#7c9cff">v{BOT_VERSION}</span>
  </div>

<script>
  const proto = location.protocol === "https:" ? "wss:" : "ws:";
  const ws = new WebSocket(proto + "//" + location.host + "/ws/stats");

  ws.onopen = () => {{
    document.getElementById("status-text").textContent = "Live";
  }};

  ws.onclose = () => {{
    document.getElementById("status-text").textContent = "Disconnected";
  }};

  ws.onmessage = (event) => {{
    const msg = JSON.parse(event.data);
    if (msg.type === "stats") {{
      const d = msg.data;
      document.getElementById("total-users").textContent = d.total_users;
      document.getElementById("active-today").textContent = d.active_today;
      document.getElementById("total-sessions").textContent = d.total_sessions;
      document.getElementById("sessions-today").textContent = d.sessions_today;
    }}
  }};
</script>
</body>
</html>
"""


# ═══════════════════════════════════════════════
#  Routes
# ═══════════════════════════════════════════════

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root():
    """Serve dashboard HTML."""
    return DASHBOARD_HTML


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "version": BOT_VERSION,
        "author": Author.NAME,
    }


@app.get("/api/stats")
async def api_stats():
    async with db.session() as s:
        stats = await crud.get_stats(s)
    return stats


@app.get("/api/sessions")
async def api_sessions(limit: int = 50):
    """Session metadata (never content)."""
    from sqlalchemy import select
    from db.models import Session

    async with db.session() as s:
        result = await s.execute(
            select(Session).order_by(Session.created_at.desc()).limit(limit)
        )
        sessions = result.scalars().all()

    return {
        "count": len(sessions),
        "sessions": [
            {
                "id": x.id,
                "user_id": x.user_id,
                "engine": x.engine,
                "dc_id": x.dc_id,
                "phone": x.phone,
                "fingerprint": x.fingerprint,
                "is_active": x.is_active,
                "created_at": x.created_at.isoformat(),
            }
            for x in sessions
        ],
    }


@app.websocket("/ws/stats")
async def ws_stats(ws: WebSocket):
    """Live stats stream."""
    await ws_manager.connect(ws)
    try:
        # Send initial stats
        async with db.session() as s:
            stats = await crud.get_stats(s)
        await ws.send_json({"type": "stats", "data": stats})

        while True:
            # Keep alive
            await asyncio.sleep(30)
            await ws.send_json({"type": "ping"})
    except WebSocketDisconnect:
        ws_manager.disconnect(ws)
    except Exception as e:
        log.error(f"WS error: {e}")
        ws_manager.disconnect(ws)


# ═══════════════════════════════════════════════
#  Entry Point
# ═══════════════════════════════════════════════

def main():
    """Run dashboard server."""
    host = "0.0.0.0"
    port = 8000

    log.info(f"Starting dashboard on http://{host}:{port}")
    log.info(f"Author: {Author.NAME} ({Author.USERNAME})")

    uvicorn.run(
        "api.dashboard:app",
        host=host,
        port=port,
        reload=False,
        log_level="info",
    )


if __name__ == "__main__":
    main()
