import os

from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

WA_TARGET_NUMBER = os.getenv("WA_TARGET_NUMBER")