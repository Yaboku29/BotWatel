import os
import logging
from pathlib import Path
from telegramProd.client import client
from telegramProd.listener import register_listener

from pipeline.pipeline import MessagePipeline

# 💡 services/logger sengaja tidak diimpor karena sudah tidak digunakan
from services.whatsapp import process
from services.database import database_service
from services.translator import process_TL

# 1️⃣ Tentukan path untuk folder logs
LOG_DIR = Path("logs")
if not LOG_DIR.exists():
    LOG_DIR.mkdir(parents=True, exist_ok=True)

# 2️⃣ Konfigurasi logging Python untuk dialihkan ke file logs/telegram.log
logging.basicConfig(
    level=logging.WARNING, 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "telegram.log", encoding="utf-8"), 
        logging.StreamHandler() 
    ]
)

async def main():
    print("⚡ Menginisialisasi Telegram Userbot Engine...")

    pipeline = MessagePipeline()

    # 🛠️ PERUBAHAN DI SINI:
    # Kita hapus/komentari baris pipeline.register(logger_service)
    # pipeline.register(logger_service) 
    
    pipeline.register(database_service)
    pipeline.register(process_TL)
    pipeline.register(process)

    register_listener(client, pipeline)
    
    me = await client.get_me()

    print(f"Login sebagai : {me.first_name}")
    print("🤖 BotWatel aktif dan mendengarkan pesan...")

    await client.run_until_disconnected()


with client:
    client.loop.run_until_complete(main())