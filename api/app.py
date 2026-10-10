"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

FastAPI application factory.
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse

from config import settings, Author, BOT_VERSION, BOT_NAME

log = logging.getLogger(__name__)


# ═══════════════════════════════════════════════
#  Lifespan (startup/shutdown)
# ═══════════════════════════════════════════════

@asynccontextmanager
async def lifespan(app: FastAPI):
    """App startup & shutdown hooks."""
    log.info("🚀 API starting...")
    yield
    log.info("🛑 API shutting down...")


# ═══════════════════════════════════════════════
#  App Factory
# ═══════════════════════════════════════════════

def create_app() -> FastAPI:
    """Build & return FastAPI app."""
    app = FastAPI(
        title=f"{BOT_NAME} — Dashboard",
        description=(
            f"Admin dashboard & monitoring API.\n\n"
            f"**Author:** [Sakil]({Author.TELEGRAM_URL}) · "
            f"[GitHub]({Author.GITHUB_URL})"
        ),
        version=BOT_VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )
    
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Register routes
    from .routes import health, stats, sessions, activity, ws
    app.include_router(health.router, tags=["health"])
    app.include_router(stats.router, prefix="/api", tags=["stats"])
    app.include_router(sessions.router, prefix="/api", tags=["sessions"])
    app.include_router(activity.router, prefix="/api", tags=["activity"])
    app.include_router(ws.router, tags=["websocket"])
    
    # Root page
    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    async def root():
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{BOT_NAME} — Dashboard</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                    background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
                    color: #e0e6ff;
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 20px;
                }}
                .container {{
                    max-width: 720px;
                    background: rgba(255, 255, 255, 0.03);
                    border: 1px solid rgba(120, 140, 255, 0.2);
                    border-radius: 16px;
                    padding: 48px;
                    backdrop-filter: blur(10px);
                }}
                h1 {{
                    font-size: 2.4rem;
                    margin-bottom: 8px;
                    background: linear-gradient(135deg, #7c9cff, #b48cff);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                }}
                .subtitle {{
                    color: #8892b0;
                    margin-bottom: 32px;
                    font-size: 1.05rem;
                }}
                .links {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 12px;
                    margin-bottom: 32px;
                }}
                a {{
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    padding: 14px 20px;
                    background: rgba(124, 156, 255, 0.08);
                    border: 1px solid rgba(124, 156, 255, 0.25);
                    border-radius: 10px;
                    color: #c5d0ff;
                    text-decoration: none;
                    font-weight: 500;
                    transition: all 0.2s;
                }}
                a:hover {{
                    background: rgba(124, 156, 255, 0.18);
                    transform: translateY(-2px);
                    color: #fff;
                }}
                .credit {{
                    padding-top: 24px;
                    border-top: 1px solid rgba(120, 140, 255, 0.15);
                    color: #8892b0;
                    font-size: 0.9rem;
                    text-align: center;
                }}
                .credit a {{
                    display: inline;
                    padding: 0;
                    background: none;
                    border: none;
                    color: #7c9cff;
                }}
                .version {{
                    display: inline-block;
                    padding: 3px 10px;
                    background: rgba(124, 156, 255, 0.15);
                    border-radius: 20px;
                    font-size: 0.85rem;
                    color: #7c9cff;
                    margin-left: 8px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🔐 {BOT_NAME}</h1>
                <p class="subtitle">Advanced Telegram Session Generator</p>
                <div class="links">
                    <a href="/docs">📖 API Documentation</a>
                    <a href="/redoc">📚 ReDoc</a>
                    <a href="/api/stats">📊 Live Stats</a>
                    <a href="/api/sessions">📂 Sessions</a>
                    <a href="/api/activity">📜 Activity</a>
                    <a href="/ws/stats">⚡ WebSocket</a>
                </div>
                <div class="credit">
                    Made with ❤️ by
                    <a href="{Author.TELEGRAM_URL}">{Author.NAME}</a>
                    · <a href="{Author.GITHUB_URL}">GitHub</a>
                    <span class="version">v{BOT_VERSION}</span>
                </div>
            </div>
        </body>
        </html>
        """
    
    return app


app = create_app()
