import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_ID = int(os.getenv("API_ID", 0))
    API_HASH = os.getenv("API_HASH", "")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    DATABASE_URL = os.getenv("DATABASE_URL", "")
    REDIS_URL = os.getenv("REDIS_URL", "")
    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "")
    OWNER_ID = int(os.getenv("OWNER_ID", 0))

config = Config()
