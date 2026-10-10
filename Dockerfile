

---

## 6. `Dockerfile` (FINAL)

```dockerfile
# Universal Session Bot
# Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
# Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
# GitHub  : https://github.com/SakilSakil699

# ── Stage 1: Builder ──
FROM python:3.11-slim AS builder

WORKDIR /build

# Install build deps
RUN apt-get update && apt-get install -y --no-install-recommends \
        gcc g++ make libffi-dev libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Stage 2: Runtime ──
FROM python:3.11-slim

LABEL maintainer="Sakil <https://t.me/YO_UR_OFFICIAL_CRUSH>"
LABEL description="Universal Session Bot — Advanced Telegram Session Generator"
LABEL version="1.0.0"

# Runtime deps
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Non-root user
RUN useradd -m -u 1000 bot && \
    mkdir -p /app/data /app/logs && \
    chown -R bot:bot /app

WORKDIR /app

# Copy Python deps from builder
COPY --from=builder /install /usr/local

# Copy project
COPY --chown=bot:bot . .

# Create dirs
RUN mkdir -p data/sessions data/tdata data/tgnet logs && \
    chown -R bot:bot /app

USER bot

# Health check
HEALTHCHECK --interval=60s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import sys; from config import settings; settings.validate(); sys.exit(0)" || exit 1

# Default: run bot
CMD ["python", "-m", "bot.main"]
