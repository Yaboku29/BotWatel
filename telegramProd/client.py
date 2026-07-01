import os
from dotenv import load_dotenv
from telethon import TelegramClient

# Membaca file .env
load_dotenv()

api_id=int(os.getenv("API_ID"))
api_hash=os.getenv("API_HASH")

#session_name akan menghasilkan file bridge.session
client=TelegramClient("watel",api_id,api_hash)