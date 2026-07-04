import sys
from pathlib import Path

# Daftarkan root folder agar bisa membaca modul client Telegram
root_path = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(root_path))

from telegramProd.client import client

async def main():
    print("==================================================")
    print("        BOTWATEL - TELEGRAM CHAT ID FETCHERS      ")
    print("==================================================")
    print("Membaca 20 obrolan terakhir akun Anda...\n")

    # Ambil 20 dialog/chat terbaru
    async for dialog in client.iter_dialogs(limit=20):
        chat_type = type(dialog.entity).__name__
        
        # Bedakan tampilan jenis chat agar mudah dibaca
        if dialog.is_user:
            type_label = "👤 DM / Private Chat"
        elif dialog.is_channel and getattr(dialog.entity, 'broadcast', False):
            type_label = "📢 Channel"
        else:
            type_label = "👥 Group"

        print(f"Nama Chat : {dialog.name}")
        print(f"Chat ID   : {dialog.id}")
        print(f"Jenis     : {type_label}")
        print("-" * 50)

with client:
    client.loop.run_until_complete(main())