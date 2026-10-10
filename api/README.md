# 🌐 API Module

**Universal Session Bot**
Author: [Sakil](https://t.me/YO_UR_OFFICIAL_CRUSH) · [GitHub](https://github.com/SakilSakil699)

FastAPI dashboard — REST endpoints + WebSocket live stats.

---

## 📂 Files

| File | Purpose |
|------|---------|
| `__init__.py` | Package exports |
| `app.py` | FastAPI app factory + root page |
| `routes/__init__.py` | Route package |
| `routes/health.py` | `/health`, `/health/deep` |
| `routes/stats.py` | `/api/stats`, `/api/stats/public` |
| `routes/sessions.py` | Session metadata (never content) |
| `routes/activity.py` | Audit logs |
| `routes/ws.py` | WebSocket live stats |
| `README.md` | This file |

---

## 🚀 Run the API

### Development

```bash
uvicorn api.app:app --reload --host 0.0.0.0 --port 8000
