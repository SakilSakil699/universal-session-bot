
#!/usr/bin/env python3
"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

Generate a secure ENCRYPTION_KEY for .env
Usage:
    python scripts/generate_key.py
"""
import secrets
import sys


def main():
    key = secrets.token_hex(32)
    
    print()
    print("=" * 55)
    print("  🔐 Universal Session Bot — Encryption Key")
    print("=" * 55)
    print()
    print(f"ENCRYPTION_KEY={key}")
    print()
    print("📋 Copy the line above into your .env file.")
    print()
    print("⚠️  IMPORTANT:")
    print("   • Never share this key")
    print("   • Never commit it to Git")
    print("   • If lost, encrypted sessions become unreadable")
    print()
    print("=" * 55)
    print("  Made with ❤️  by Sakil (@YO_UR_OFFICIAL_CRUSH)")
    print("=" * 55)
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
