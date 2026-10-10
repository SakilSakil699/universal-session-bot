
#!/usr/bin/env bash
#
# Universal Session Bot
# Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
# Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
# GitHub  : https://github.com/SakilSakil699
#
# Clone external vendor libraries into vendors/
# Usage: bash scripts/setup_vendors.sh

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
VENDORS_DIR="$ROOT_DIR/vendors"

echo ""
echo "======================================================="
echo "  🔐 Universal Session Bot — Vendors Setup"
echo "  by Sakil (@YO_UR_OFFICIAL_CRUSH)"
echo "======================================================="
echo ""

mkdir -p "$VENDORS_DIR"
cd "$VENDORS_DIR"

# ── tgconvert ────────────────────────────────────
if [ ! -d "tgconvert" ]; then
    echo -e "${CYAN}[1/3]${NC} Cloning tgconvert..."
    git clone --depth 1 https://github.com/botiratory/tgconvert.git 2>/dev/null || {
        echo -e "${YELLOW}⚠️  tgconvert clone failed — skipping${NC}"
    }
else
    echo -e "${GREEN}[1/3]${NC} tgconvert already present"
fi

# ── AndroidTelePorter ────────────────────────────
if [ ! -d "AndroidTelePorter" ]; then
    echo -e "${CYAN}[2/3]${NC} Cloning AndroidTelePorter..."
    git clone --depth 1 https://github.com/Slavik_27/AndroidTelePorter.git 2>/dev/null || {
        echo -e "${YELLOW}⚠️  AndroidTelePorter clone failed — skipping${NC}"
    }
else
    echo -e "${GREEN}[2/3]${NC} AndroidTelePorter already present"
fi

# ── tdata_reader ─────────────────────────────────
if [ ! -d "tdata_reader" ]; then
    echo -e "${CYAN}[3/3]${NC} Cloning tdata_reader..."
    git clone --depth 1 https://github.com/dem0n1x/tdata-reader.git 2>/dev/null || {
        echo -e "${YELLOW}⚠️  tdata_reader clone failed — skipping${NC}"
    }
else
    echo -e "${GREEN}[3/3]${NC} tdata_reader already present"
fi

echo ""
echo "======================================================="
echo -e "${GREEN}  ✅ Vendors setup complete${NC}"
echo "======================================================="
echo ""
echo "  📁 Location: $VENDORS_DIR"
echo ""
echo "  ⚠️  Some vendors may need manual installation."
echo "     Check each vendor's README for details."
echo ""
echo "  Made with ❤️  by Sakil (@YO_UR_OFFICIAL_CRUSH)"
echo ""
