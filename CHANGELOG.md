
# 📝 Changelog

**Universal Session Bot**
Author: [Sakil](https://t.me/YO_UR_OFFICIAL_CRUSH) · [GitHub](https://github.com/SakilSakil699)

All notable changes to this project.

Format based on [Keep a Changelog](https://keepachangelog.com/).
Versioning: [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

### Planned
- Multi-language support (Hindi, English)
- Session health monitoring
- Auto session rotation
- Telegram Mini App dashboard
- Post-quantum encryption (Kyber)

---

## [1.0.0] - 2026-01-15

### 🎉 Initial Release

#### Added — Core
- `UniversalSession` dataclass — common denominator for all formats
- `SessionConverter` — bidirectional conversion between 9+ formats
- `SessionParser` — auto-detect any session format
- `SessionUtils` — validation, fingerprint, extraction helpers
- Custom exception hierarchy

#### Added — Crypto
- AES-256-GCM encryption for session storage
- Argon2id key derivation (64 MB, 4 iterations)
- Zero-knowledge vault architecture
- Timing-attack-safe comparison
- Secure random generation via `secrets`

#### Added — Engines
- **Telethon** engine — stable, recommended
- **Pyrogram** engine — fast, clean API
- **Ferogram** engine — Rust core, experimental
- **GramJS** worker — Node.js subprocess
- Unified `LoginResult` interface
- Factory pattern (`get_engine`)

#### Added — Handlers
- `/start` — welcome menu
- `/help` — command reference
- `/about` — bot info + credits
- `/newsession` — session generation flow
- `/mysessions` — saved sessions
- `/cancel` — abort current flow
- `/admin` — owner panel
- Callback handlers for all inline buttons

#### Added — Keyboards
- Main menu (grid layout)
- Engine selection
- Format selection
- Confirmation dialogs
- Back buttons

#### Added — Utils
- `Validators` — phone, OTP, session, file validation
- `rate_limiter` — sliding window per-user
- `FileHandler` — safe download/upload with size limits
- `TGHelpers` — mentions, message splitting, safe edits
- Colored logger with rotating file handler

#### Added — Database
- Async SQLAlchemy 2.0 models
- `User`, `Session`, `ActivityLog` tables
- Full CRUD operations
- Aggregate stats queries
- Deduplication via fingerprint

#### Added — API
- FastAPI dashboard (`api/dashboard.py`)
- REST endpoints for stats, sessions, activity
- WebSocket live stats stream
- HTML landing page with dark theme
- CORS + optional bearer auth

#### Added — Vendors
- `tgconvert` — tdata/pyro/telethon conversion
- `AndroidTelePorter` — tgnet support
- `tdata_reader` — tdata → telethon
- Self-contained folder structure

#### Added — Scripts
- `generate_key.py` — secure key generator
- `init_db.py` — database initializer
- `setup_vendors.sh` — clone external libs
- `run.sh` — quick start

#### Added — Tests
- `conftest.py` — shared fixtures
- `test_converters.py` — conversion roundtrips
- `test_crypto.py` — encryption tests
- `test_validators.py` — input validation
- `test_session_utils.py` — utility functions
- `test_universal_session.py` — dataclass tests
- `test_engines.py` — engine mocks

#### Added — CI/CD
- `test.yml` — pytest on Python 3.10/3.11/3.12
- `security.yml` — TruffleHog + Bandit + CodeQL + Trivy
- `docker.yml` — build & push to GHCR
- `deploy.yml` — SSH/Railway deployment

#### Added — Docs
- `SETUP.md` — installation guide
- `FORMATS.md` — all session formats spec
- `ARCHITECTURE.md` — system design
- `SECURITY.md` — threat model
- `FAQ.md` — common questions
- `API.md` — internal API reference

#### Security
- ✅ AES-256-GCM at rest
- ✅ Argon2id KDF
- ✅ Timing-safe compare
- ✅ Rate limiting
- ✅ Audit trail
- ✅ Path traversal protection
- ✅ HTML escaping
- ✅ Never logs secrets

#### Performance
- ✅ uvloop (2-4x faster)
- ✅ Async SQLAlchemy
- ✅ Connection pooling
- ✅ Conditional engine imports
- ✅ In-memory FSM

---

## 🔗 Links

- [Telegram](https://t.me/YO_UR_OFFICIAL_CRUSH) — Sakil
- [GitHub](https://github.com/SakilSakil699) — Profile
- [Repo](https://github.com/SakilSakil699/universal-session-bot) — Source

---

**Made with ❤️ by [Sakil](https://t.me/YO_UR_OFFICIAL_CRUSH)**
