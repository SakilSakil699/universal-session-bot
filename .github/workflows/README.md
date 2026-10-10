# ⚙️ GitHub Workflows

**Universal Session Bot**
Author: [Sakil](https://t.me/YO_UR_OFFICIAL_CRUSH) · [GitHub](https://github.com/SakilSakil699)

CI/CD pipelines for the bot.

---

## 📂 Workflows

| File | Trigger | Purpose |
|------|---------|---------|
| `test.yml` | Push, PR | Run pytest on Python 3.10/3.11/3.12 |
| `security.yml` | Push, weekly | Secret scan + CodeQL + pip-audit |
| `docker.yml` | Tag `v*` | Build & push Docker image to GHCR |
| `deploy.yml` | Tag `v*` | Deploy to production (SSH/Railway) |

---

## 🧪 Tests Workflow

**Triggers:** Every push + every PR

**Matrix:**
- Python 3.10
- Python 3.11
- Python 3.12

**Steps:**
1. Install dependencies
2. Run `pytest tests/`
3. Upload coverage to Codecov

**Badge:**
```markdown
![Tests](https://github.com/SakilSakil699/universal-session-bot/actions/workflows/test.yml/badge.svg)
