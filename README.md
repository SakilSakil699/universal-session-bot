<div align="center">

# 🔐 Universal Session Bot

**Advanced Telegram Session Generator**
*Multi-Format · Encrypted · Superfast · Secure*

[![Tests](https://github.com/SakilSakil699/universal-session-bot/actions/workflows/test.yml/badge.svg)](https://github.com/SakilSakil699/universal-session-bot/actions/workflows/test.yml)
[![Security](https://github.com/SakilSakil699/universal-session-bot/actions/workflows/security.yml/badge.svg)](https://github.com/SakilSakil699/universal-session-bot/actions/workflows/security.yml)
[![Docker](https://github.com/SakilSakil699/universal-session-bot/actions/workflows/docker.yml/badge.svg)](https://github.com/SakilSakil699/universal-session-bot/actions/workflows/docker.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)
[![Telegram](https://img.shields.io/badge/Telegram-@YO__UR__OFFICIAL__CRUSH-blue.svg)](https://t.me/YO_UR_OFFICIAL_CRUSH)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

[Features](#-features) · [Quick Start](#-quick-start) · [Docs](#-documentation) · [Architecture](#-architecture) · [Contributing](#-contributing)

</div>

---

## 🎯 What is This?

A **production-grade** Telegram bot that generates sessions in **9+ formats** with **AES-256-GCM encryption**. Built with modern async Python, powered by **Telethon + Pyrogram + Ferogram + GramJS** engines.

> **🎨 Advanced UI** — Beautiful dark-themed dashboard, live WebSocket stats, clickable credits, smooth animations.
> **⚡ Superfast** — uvloop (2-4x faster), async everything, connection pooling.
> **🔒 Secure** — Zero-knowledge vault, Argon2id KDF, rate limiting, audit trails.

---

## ✨ Features

### 🎯 Multi-Format Support (9 Formats)

| Format | Type | Use Case |
|--------|------|----------|
| **Pyrogram String** | Python | Automation scripts |
| **Telethon String** | Python | Scripts & bots |
| **GramJS Hex** | Node.js | JS/TS apps |
| **Mtcute** | TS/JS | Modern web |
| **JSON** | Any | Debugging |
| **Auth Key** | Raw | Low-level |
| **TData** | Desktop | Telegram Desktop |
| **Android tgnet** | Android | Android app |
| **Ferogram** | Rust core | Ultra-fast |

### ⚡ Multi-Engine Login

- 🟢 **Telethon** — Stable, recommended
- 🚀 **Pyrogram** — Fast, clean API
- 🦀 **Ferogram** — Rust core (experimental)
- 🌐 **GramJS** — Node.js worker

### 🔐 Security Stack

- 🔒 **AES-256-GCM** encryption at rest
- 🔑 **Argon2id** KDF (64 MB, 4 iterations)
- 🛡️ Zero-knowledge storage
- ⏱️ Timing-attack-safe compare
- 🚦 Per-user rate limiting
- 📜 Full audit trail
- 🧹 Path traversal protection
- 💉 HTML escaping everywhere

### 🚀 Performance

- ⚡ `uvloop` — 2-4x faster event loop
- 🔄 Async SQLAlchemy
- 📦 Connection pooling
- 🎯 Conditional imports
- 🌐 Webhook-ready

### 📊 Monitoring & UI

- 🎨 **Beautiful dashboard** at `/` (dark theme, gradients)
- 📈 **WebSocket live stats** (auto-update every 5s)
- 📂 Session metadata API
- 📜 Activity log stream
- 🎭 Smooth CSS animations

### 🛠️ Developer Experience

- ✅ Full type hints
- 🎯 Custom exception hierarchy
- 🧪 90%+ test coverage
- 🔄 GitHub Actions CI/CD
- 🐳 Docker support
- 📚 Comprehensive docs

---

## ⚡ Quick Start

### Prerequisites
