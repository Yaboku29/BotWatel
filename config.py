import os

from dotenv import load_dotenv

load_dotenv()

# Telegram
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

# WhatsApp
WA_TARGET_NUMBER = os.getenv("WA_TARGET_NUMBER")
WA_API_URL = os.getenv(
    "WA_API_URL",
    "http://localhost:3000"
)

# Database
DATABASE_PATH = os.getenv(
    "DATABASE_PATH",
    "database/botwatel.db"
)

# Logging
LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO"
)