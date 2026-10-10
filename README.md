<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,20,24&height=200&section=header&text=Universal%20Session%20Bot&fontSize=50&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=Advanced%20Telegram%20Session%20Generator&descAlignY=58&descSize=18" width="100%"/>

**🔐 Multi-Format · ⚡ Superfast · 🔒 Encrypted · 🎨 Beautiful UI**

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&size=18&pause=1000&color=7C9CFF&center=true&vCenter=true&width=600&lines=9%2B+Session+Formats+Supported;Telethon+%7C+Pyrogram+%7C+Ferogram+%7C+GramJS;AES-256-GCM+Encrypted+Storage;Built+with+%E2%9D%A4%EF%B8%8F+by+Sakil)](https://github.com/SakilSakil699/universal-session-bot)

<p>
<a href="https://github.com/SakilSakil699/universal-session-bot/stargazers"><img src="https://img.shields.io/github/stars/SakilSakil699/universal-session-bot?style=for-the-badge&logo=github&color=yellow" alt="Stars"/></a>
<a href="https://github.com/SakilSakil699/universal-session-bot/network/members"><img src="https://img.shields.io/github/forks/SakilSakil699/universal-session-bot?style=for-the-badge&logo=github&color=blue" alt="Forks"/></a>
<a href="https://github.com/SakilSakil699/universal-session-bot/issues"><img src="https://img.shields.io/github/issues/SakilSakil699/universal-session-bot?style=for-the-badge&logo=github&color=red" alt="Issues"/></a>
<a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License"/></a>
</p>

<p>
<a href="https://github.com/SakilSakil699/universal-session-bot/actions/workflows/test.yml"><img src="https://github.com/SakilSakil699/universal-session-bot/actions/workflows/test.yml/badge.svg" alt="Tests"/></a>
<a href="https://github.com/SakilSakil699/universal-session-bot/actions/workflows/security.yml"><img src="https://github.com/SakilSakil699/universal-session-bot/actions/workflows/security.yml/badge.svg" alt="Security"/></a>
<a href="https://github.com/SakilSakil699/universal-session-bot/actions/workflows/docker.yml"><img src="https://github.com/SakilSakil699/universal-session-bot/actions/workflows/docker.yml/badge.svg" alt="Docker"/></a>
</p>

<p>
<a href="https://t.me/YO_UR_OFFICIAL_CRUSH"><img src="https://img.shields.io/badge/Telegram-Contact-blue?style=for-the-badge&logo=telegram" alt="Telegram"/></a>
<a href="https://github.com/SakilSakil699"><img src="https://img.shields.io/badge/GitHub-Follow-black?style=for-the-badge&logo=github" alt="GitHub"/></a>
</p>

</div>

---

## 🎬 What Is This?

> **Universal Session Bot** ek **production-grade** Telegram bot hai jo **9+ session formats** generate karta hai — **Telethon**, **Pyrogram**, **Ferogram** (Rust core), **GramJS**, **Mtcute**, **TData**, **Android tgnet**, aur more.
>
> Sab sessions **AES-256-GCM** se encrypt hote hain, **Argon2id** se key derive hoti hai, aur ek **zero-knowledge vault** me store hote hain. Full async Python, **uvloop**-powered, aur ek **beautiful dark-themed dashboard** ke saath.

### 🎯 Why Choose This Bot?

| Feature | Others | **Universal Session Bot** |
|---------|--------|--------------------------|
| Formats supported | 2-3 | **9+** ✨ |
| Encryption at rest | ❌ | ✅ AES-256-GCM |
| KDF | ❌ | ✅ Argon2id |
| Multi-engine login | ❌ | ✅ Telethon + Pyrogram + Ferogram |
| Web dashboard | ❌ | ✅ FastAPI + WebSocket |
| Live stats | ❌ | ✅ Real-time |
| Rate limiting | ❌ | ✅ Per-user |
| Audit trail | ❌ | ✅ Full |
| Tests | ❌ | ✅ 90%+ coverage |
| CI/CD | ❌ | ✅ GitHub Actions |
| Docker | ❌ | ✅ One command |

---

## ✨ Feature Deep-Dive

<table>
<tr>
<td width="50%">

### 🎯 9+ Session Formats

- 🔹 **Pyrogram String**
- 🔹 **Telethon String**
- 🔹 **GramJS Hex**
- 🔹 **Mtcute v3**
- 🔹 **JSON**
- 🔑 **Auth Key**
- 📦 **TData** (Desktop)
- 📦 **Android tgnet**
- 🦀 **Ferogram** (Rust)

</td>
<td width="50%">

### ⚡ Multi-Engine Login

- 🟢 **Telethon** — Stable
- 🚀 **Pyrogram** — Fast
- 🦀 **Ferogram** — Rust core
- 🌐 **GramJS** — Node.js

### 🔐 Security

- AES-256-GCM
- Argon2id (64 MB)
- Rate limiting
- Audit logs
- Path safety
- HTML escaping

</td>
</tr>
</table>

---

## 🚀 Deployment Guides

> **Har platform ke liye step-by-step guide with all commands.**

### 📱 Option 1: Termux (Android)

**Termux pe bot chalane ka complete guide:**

#### Step 1 — Install Termux

Play Store se **Termux** install karo, ya [F-Droid](https://f-droid.org/en/packages/com.termux/) se lo (recommended — newer).

#### Step 2 — Update Packages

```bash
pkg update && pkg upgrade -y
```

#### Step 3 — Install Dependencies

```bash
pkg install -y python git clang libffi openssl rust binutils
```

**Note:** `rust` package Ferogram build ke liye zaroori hai. Agar nahi chahiye, skip kar sakte ho.

#### Step 4 — Install pip

```bash
pkg install -y python-pip
pip install --upgrade pip
```

#### Step 5 — Clone Repository

```bash
cd ~
git clone https://github.com/SakilSakil699/universal-session-bot.git
cd universal-session-bot
```

#### Step 6 — Install Python Packages

```bash
pip install -r requirements.txt
```

**Agar Ferogram fail ho** (common Termux issue):

```bash
# Ferogram skip karo
sed -i 's/^ferogram/#ferogram/' requirements.txt
pip install -r requirements.txt
```

#### Step 7 — Setup .env

```bash
cp .env.example .env
nano .env
```

Fill karo:
```
API_ID=your_id
API_HASH=your_hash
BOT_TOKEN=your_token
OWNER_ID=your_id
ENCRYPTION_KEY=your_key
DATABASE_URL=sqlite+aiosqlite:///./data/sessions.db
```

**Save karne ke liye:** `Ctrl+X` → `Y` → `Enter`

#### Step 8 — Generate Key

```bash
python scripts/generate_key.py
```

Output copy karke `.env` me `ENCRYPTION_KEY=` ke aage paste karo.

#### Step 9 — Init Database

```bash
python scripts/init_db.py
```

#### Step 10 — Run Bot

```bash
python -m bot.main
```

**Background me chalane ke liye:**

```bash
# Termux ke background me
nohup python -m bot.main > logs/bot.log 2>&1 &

# Check running
ps aux | grep bot.main

# Kill
pkill -f bot.main
```

**Termux me wake-lock:**

```bash
# Screen off hone par bhi chalta rahe
termux-wake-lock

# Disable
termux-wake-unlock
```

**Auto-start on boot (advanced):**

```bash
mkdir -p ~/.termux/boot
cat > ~/.termux/boot/start-bot.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/sh
termux-wake-lock
cd ~/universal-session-bot
python -m bot.main > logs/bot.log 2>&1 &
EOF
chmod +x ~/.termux/boot/start-bot.sh
```

Termux:Boot app install karo (F-Droid se).

---

### 🖥️ Option 2: VPS (Ubuntu/Debian)

**Recommended VPS providers:** Hetzner, Contabo, DigitalOcean, Vultr

#### Step 1 — SSH Login

```bash
ssh root@your_server_ip
```

#### Step 2 — Update System

```bash
apt update && apt upgrade -y
```

#### Step 3 — Install Dependencies

```bash
apt install -y python3.11 python3.11-venv python3-pip \
    git postgresql redis-server nginx \
    build-essential libssl-dev libffi-dev
```

#### Step 4 — Create Bot User

```bash
adduser --disabled-password --gecos "" botuser
usermod -aG sudo botuser
su - botuser
```

#### Step 5 — Clone Repository

```bash
git clone https://github.com/SakilSakil699/universal-session-bot.git
cd universal-session-bot
```

#### Step 6 — Setup Python Env

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 7 — Setup PostgreSQL

```bash
sudo -u postgres psql
```

Inside psql:
```sql
CREATE DATABASE sessionbot;
CREATE USER botuser WITH PASSWORD 'strong_password_here';
GRANT ALL PRIVILEGES ON DATABASE sessionbot TO botuser;
ALTER DATABASE sessionbot OWNER TO botuser;
\q
```

#### Step 8 — Setup .env

```bash
cp .env.example .env
nano .env
```

Fill karo:
```
DATABASE_URL=postgresql+asyncpg://botuser:strong_password_here@localhost:5432/sessionbot
REDIS_URL=redis://localhost:6379/0
ENCRYPTION_KEY=your_generated_key
```

#### Step 9 — Init DB

```bash
python scripts/init_db.py
```

#### Step 10 — Setup Systemd Service

```bash
sudo nano /etc/systemd/system/sessionbot.service
```

Paste karo:
```ini
[Unit]
Description=Universal Session Bot
After=network.target postgresql.service redis.service

[Service]
Type=simple
User=botuser
WorkingDirectory=/home/botuser/universal-session-bot
Environment="PATH=/home/botuser/universal-session-bot/venv/bin"
ExecStart=/home/botuser/universal-session-bot/venv/bin/python -m bot.main
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable & start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable sessionbot
sudo systemctl start sessionbot
sudo systemctl status sessionbot
```

**Logs dekho:**
```bash
sudo journalctl -u sessionbot -f
```

**Restart/Stop:**
```bash
sudo systemctl restart sessionbot
sudo systemctl stop sessionbot
```

#### Step 11 — Dashboard (Optional)

```bash
sudo nano /etc/systemd/system/sessionbot-dashboard.service
```

```ini
[Unit]
Description=Universal Session Bot Dashboard
After=network.target

[Service]
Type=simple
User=botuser
WorkingDirectory=/home/botuser/universal-session-bot
Environment="PATH=/home/botuser/universal-session-bot/venv/bin"
ExecStart=/home/botuser/universal-session-bot/venv/bin/uvicorn api.dashboard:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable sessionbot-dashboard
sudo systemctl start sessionbot-dashboard
```

#### Step 12 — Nginx Reverse Proxy (Optional)

```bash
sudo nano /etc/nginx/sites-available/sessionbot
```

```nginx
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/sessionbot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

**SSL (Let's Encrypt):**
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your_domain.com
```

---

### 🐳 Option 3: Docker (Recommended for VPS)

**Sabse easy — one command deploy.**

#### Step 1 — Install Docker

```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker
```

#### Step 2 — Clone & Configure

```bash
git clone https://github.com/SakilSakil699/universal-session-bot.git
cd universal-session-bot
cp .env.example .env
nano .env
```

#### Step 3 — Deploy

```bash
docker-compose up -d
```

**Services:**
- `bot` — Telegram bot
- `dashboard` — API + WebSocket
- `postgres` — Database
- `redis` — Cache

#### Step 4 — Verify

```bash
docker-compose ps
docker-compose logs -f bot
```

#### Step 5 — Manage

```bash
# Stop
docker-compose down

# Restart
docker-compose restart

# Update
git pull
docker-compose up -d --build

# Logs
docker-compose logs -f bot
docker-compose logs -f dashboard

# Shell into container
docker-compose exec bot bash
```

---

### ☁️ Option 4: Free Hosting

#### Railway.app (Recommended)

**Free tier: 500 hours/month + $5 credit**

1. [railway.app](https://railway.app) → Sign up with GitHub
2. **New Project** → **Deploy from GitHub repo**
3. Select `universal-session-bot`
4. **Add PostgreSQL** plugin
5. **Variables** tab → add:
   ```
   API_ID=...
   API_HASH=...
   BOT_TOKEN=...
   OWNER_ID=...
   ENCRYPTION_KEY=...
   DATABASE_URL=${{Postgres.DATABASE_URL}}
   ```
6. **Settings** → **Deploy** → Auto-deploy from GitHub

#### Render.com

**Free tier: 750 hours/month**

1. [render.com](https://render.com) → Sign up
2. **New** → **Web Service** → Connect GitHub
3. **Build Command:** `pip install -r requirements.txt`
4. **Start Command:** `python -m bot.main`
5. Add environment variables
6. Add PostgreSQL database

#### Fly.io

**Free tier: 3 shared VMs**

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login
flyctl auth login

# Launch
cd universal-session-bot
flyctl launch

# Set secrets
flyctl secrets set API_ID=... API_HASH=... BOT_TOKEN=...

# Deploy
flyctl deploy
```

---

### 🖥️ Option 5: Windows

#### Step 1 — Install Python

[python.org](https://python.org) se Python 3.11+ install karo. **"Add to PATH"** checkbox check karo.

#### Step 2 — Install Git

[git-scm.com](https://git-scm.com/download/win) se install karo.

#### Step 3 — Open PowerShell

```powershell
git clone https://github.com/SakilSakil699/universal-session-bot.git
cd universal-session-bot
```

#### Step 4 — Virtual Environment

```powershell
python -m venv venv
venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 5 — Setup .env

```powershell
copy .env.example .env
notepad .env
```

#### Step 6 — Generate Key & Init DB

```powershell
python scripts\generate_key.py
python scripts\init_db.py
```

#### Step 7 — Run

```powershell
python -m bot.main
```

---

### 🍎 Option 6: macOS

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install deps
brew install python@3.11 git postgresql redis

# Clone & setup
git clone https://github.com/SakilSakil699/universal-session-bot.git
cd universal-session-bot
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Config
cp .env.example .env
nano .env

# Init & run
python scripts/init_db.py
python -m bot.main
```

---

## 🎮 Bot Commands Guide

### User Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/start` | Welcome menu | `/start` |
| `/help` | Help & all commands | `/help` |
| `/about` | Bot info & credits | `/about` |
| `/newsession` | Create new session | `/newsession` |
| `/mysessions` | View saved sessions | `/mysessions` |
| `/cancel` | Cancel current flow | `/cancel` |

### Owner Commands

| Command | Description | Access |
|---------|-------------|--------|
| `/admin` | Admin panel | Owner only |
| `/stats` | Bot statistics | Owner only |
| `/broadcast` | Message all users | Owner only |
| `/ban <id>` | Ban user | Owner only |
| `/unban <id>` | Unban user | Owner only |

### Session Generation Flow

```
/start
  │
  ▼
Choose Engine (Telethon / Pyrogram / Ferogram)
  │
  ▼
Send Phone (+919876543210)
  │
  ▼
Send OTP (1 2 3 4 5 — with spaces!)
  │
  ▼
[2FA Password if enabled]
  │
  ▼
Choose Format (Pyrogram / Telethon / GramJS / etc.)
  │
  ▼
✅ Session + Credit Footer
```

---

## 🛠️ All Commands Cheatsheet

### Setup Commands

```bash
# Clone
git clone https://github.com/SakilSakil699/universal-session-bot.git
cd universal-session-bot

# Virtual env
python -m venv venv
source venv/bin/activate           # Linux/Mac
venv\Scripts\activate              # Windows

# Install
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Config
cp .env.example .env
nano .env
```

### Generate & Init Commands

```bash
# Generate encryption key
python scripts/generate_key.py

# Init database
python scripts/init_db.py

# Setup vendors
bash scripts/setup_vendors.sh

# Make scripts executable
chmod +x scripts/*.sh scripts/*.py
```

### Run Commands

```bash
# Run bot
python -m bot.main

# Run dashboard
python -m api.dashboard

# Or via uvicorn
uvicorn api.dashboard:app --host 0.0.0.0 --port 8000

# Quick run (all-in-one)
bash scripts/run.sh
```

### Docker Commands

```bash
# Build & start
docker-compose up -d

# Logs
docker-compose logs -f bot
docker-compose logs -f dashboard

# Stop
docker-compose down

# Restart
docker-compose restart

# Update
git pull && docker-compose up -d --build

# Shell into bot
docker-compose exec bot bash

# Rebuild single service
docker-compose up -d --build bot
```

### Test Commands

```bash
# All tests
pytest tests/ -v

# Specific file
pytest tests/test_engines.py -v

# With coverage
pytest tests/ --cov=. --cov-report=html

# Linting
ruff check .
black --check .
isort --check-only .

# Auto-fix
ruff check --fix .
black .
isort .
```

### Maintenance Commands

```bash
# View logs
tail -f logs/bot.log

# Search errors
grep "ERROR" logs/bot.log

# Clean logs
rm -f logs/*.log*

# Clean data
rm -rf data/sessions/* data/tdata/* data/tgnet/*

# Backup DB
pg_dump sessionbot > backup.sql

# Restore DB
psql sessionbot < backup.sql

# Systemd (VPS)
sudo systemctl restart sessionbot
sudo systemctl status sessionbot
sudo journalctl -u sessionbot -f
```

---

## 📊 Configuration Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `API_ID` | ✅ | — | From my.telegram.org |
| `API_HASH` | ✅ | — | From my.telegram.org |
| `BOT_TOKEN` | ✅ | — | From @BotFather |
| `OWNER_ID` | ✅ | — | Your Telegram ID |
| `ENCRYPTION_KEY` | ✅ | — | 64-char hex |
| `DATABASE_URL` | ✅ | postgres local | DB connection |
| `REDIS_URL` | ❌ | redis local | Cache |
| `ADMIN_IDS` | ❌ | — | Comma-separated |
| `LOG_LEVEL` | ❌ | INFO | INFO/DEBUG/WARNING |
| `RATE_LIMIT_PER_MINUTE` | ❌ | 5 | Per-user |
| `MAX_SESSIONS_PER_USER` | ❌ | 10 | |
| `ENABLE_FEROGRAM` | ❌ | false | Rust engine |
| `ENABLE_GRAMJS` | ❌ | false | Node.js worker |
| `ENABLE_TDATA` | ❌ | false | tdata/tgnet |

---

## 🐛 Troubleshooting

<details>
<summary><b>❌ Config validation failed</b></summary>

Missing env vars. Check `.env`:

```bash
python -c "from config import settings; settings.validate()"
```
</details>

<details>
<summary><b>❌ Invalid BOT_TOKEN</b></summary>

Token revoked. Get new from @BotFather:

```
/mybots → select bot → API Token → Revoke
```
</details>

<details>
<summary><b>❌ Could not connect to PostgreSQL</b></summary>

Check:
```bash
sudo systemctl status postgresql
psql -U botuser -d sessionbot -h localhost
```
</details>

<details>
<summary><b>❌ Termux: pip install ferogram fails</b></summary>

Ferogram needs Rust. Skip it:

```bash
sed -i 's/^ferogram/#ferogram/' requirements.txt
pip install -r requirements.txt
```
</details>

<details>
<summary><b>❌ FloodWait errors</b></summary>

Telegram rate-limited you. Wait the seconds shown. Use different engine.

</details>

<details>
<summary><b>❌ ModuleNotFoundError</b></summary>

Virtual env not activated:

```bash
source venv/bin/activate
```
</details>

<details>
<summary><b>❌ uvloop not installed</b></summary>

Optional. Linux/Mac only:

```bash
pip install uvloop
```
</details>

<details>
<summary><b>❌ Bot silent</b></summary>

1. Check `logs/bot.log`
2. Set `LOG_LEVEL=DEBUG`
3. Verify only one instance runs

</details>

---

## 🔒 Security Notes

**Never commit these files:**

```
❌ .env
❌ *.session
❌ auth_key.txt
❌ *.key
```

**If leaked:**
1. Revoke BOT_TOKEN via @BotFather
2. Rotate ENCRYPTION_KEY
3. Force user re-login

**Best practices:**
- Use 2FA on server
- Enable firewall (ufw)
- Keep deps updated
- Review logs weekly

---

## 📖 Documentation

| Doc | Description |
|-----|-------------|
| [SETUP.md](docs/SETUP.md) | Full installation |
| [FORMATS.md](docs/FORMATS.md) | All format specs |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design |
| [SECURITY.md](docs/SECURITY.md) | Threat model |
| [FAQ.md](docs/FAQ.md) | Common questions |
| [API.md](docs/API.md) | Internal API |

---

## 🧪 Testing

```bash
pytest tests/ -v --cov=.
```

Coverage: **90%+**

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

```bash
git checkout -b feature/your-feature
# Make changes
pytest tests/ -v
git commit -m "feat: your feature"
git push origin feature/your-feature
```

---

## ⚠️ Disclaimer

**For legitimate use only.**

✅ **Allowed:** Own accounts, education, research
❌ **Prohibited:** Others' accounts, illegal use (IT Act 66C/D)

Author not responsible for misuse.

---

## 📄 License

MIT © [Sakil](https://t.me/YO_UR_OFFICIAL_CRUSH)

---

<div align="center">

### 👨‍💻 Author

**Sakil**

[![Telegram](https://img.shields.io/badge/Telegram-@YO__UR__OFFICIAL__CRUSH-blue?style=for-the-badge&logo=telegram)](https://t.me/YO_UR_OFFICIAL_CRUSH)
[![GitHub](https://img.shields.io/badge/GitHub-SakilSakil699-black?style=for-the-badge&logo=github)](https://github.com/SakilSakil699)

---

### ⭐ Star this repo if you find it useful!

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,20,24&height=120&section=footer&text=Made%20with%20%E2%9D%A4%EF%B8%8F%20by%20Sakil&fontSize=24&fontColor=ffffff&animation=fadeIn" width="100%"/>

</div>
