#!/usr/bin/env bash
#
# Universal Session Bot
# Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
# Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
# GitHub  : https://github.com/SakilSakil699
#
# Quick run script — activates venv and starts bot.
# Usage: bash scripts/run.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$ROOT_DIR"

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

echo ""
echo "======================================================="
echo "  🔐 Universal Session Bot"
echo "  by Sakil (@YO_UR_OFFICIAL_CRUSH)"
echo "======================================================="
echo ""

# Check venv
if [ ! -d "venv" ] && [ ! -d ".venv" ]; then
    echo -e "${CYAN}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Check .env
if [ ! -f ".env" ]; then
    echo -e "${CYAN}Creating .env from template...${NC}"
    cp .env.example .env
    echo "⚠️  Edit .env and fill in API_ID, API_HASH, BOT_TOKEN, OWNER_ID, ENCRYPTION_KEY"
    exit 1
fi

# Install deps
echo -e "${CYAN}Checking dependencies...${NC}"
pip install -q -r requirements.txt

# Run bot
echo -e "${GREEN}Starting bot...${NC}"
echo ""
python -m bot.main
