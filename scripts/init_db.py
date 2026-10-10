
#!/usr/bin/env python3
"""
Universal Session Bot
Author  : Sakil (@YO_UR_OFFICIAL_CRUSH)
Telegram: https://t.me/YO_UR_OFFICIAL_CRUSH
GitHub  : https://github.com/SakilSakil699

Initialize the database — create all tables.
Usage:
    python scripts/init_db.py
"""
import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


async def main():
    from config import settings, Emojis
    from db import db
    from db.models import Base
    
    print()
    print("=" * 55)
    print(f"  {Emojis.SHIELD} Universal Session Bot — DB Init")
    print("=" * 55)
    print()
    
    # Validate config
    try:
        settings.validate()
        print(f"{Emojis.CHECK} Config validated")
    except Exception as e:
        print(f"{Emojis.CROSS} Config error: {e}")
        sys.exit(1)
    
    # Show DB target
    db_url = settings.DATABASE_URL.split("@")[-1]
    print(f"{Emojis.INFO} Target: {db_url}")
    print()
    
    # Init
    try:
        await db.init()
        print(f"{Emojis.CHECK} Tables created:")
        for table in Base.metadata.tables.keys():
            print(f"     • {table}")
        print()
        print(f"{Emojis.SUCCESS} Database ready!")
    except Exception as e:
        print(f"{Emojis.CROSS} Init failed: {e}")
        sys.exit(1)
    finally:
        await db.close()
    
    print()
    print("=" * 55)
    print("  Made with ❤️  by Sakil (@YO_UR_OFFICIAL_CRUSH)")
    print("=" * 55)
    print()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
