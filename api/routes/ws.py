"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

WebSocket endpoints for live stats.
"""
import asyncio
import json
from datetime import datetime

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from db import db, crud
from utils import get_logger

log = get_logger("api.ws")
router = APIRouter()


class ConnectionManager:
    """Track active WebSocket connections."""
    def __init__(self):
        self.active: set[WebSocket] = set()

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.add(ws)
        log.info(f"WS connected. Total: {len(self.active)}")

    def disconnect(self, ws: WebSocket):
        self.active.discard(ws)
        log.info(f"WS disconnected. Total: {len(self.active)}")

    async def broadcast(self, message: dict):
        """Send to all connected clients."""
        dead = []
        for ws in self.active:
            try:
                await ws.send_json(message)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(ws)


manager = ConnectionManager()


@router.websocket("/ws/stats")
async def ws_stats(ws: WebSocket):
    """
    Live stats WebSocket.
    Pushes stats every 5 seconds.
    """
    await manager.connect(ws)
    try:
        while True:
            try:
                async with db.session() as s:
                    stats = await crud.get_stats(s)
                await ws.send_json({
                    "type": "stats",
                    "data": stats,
                    "time": datetime.utcnow().isoformat(),
                })
            except Exception as e:
                await ws.send_json({
                    "type": "error",
                    "error": str(e),
                })
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        manager.disconnect(ws)
    except Exception as e:
        log.error(f"WS error: {e}")
        manager.disconnect(ws)
