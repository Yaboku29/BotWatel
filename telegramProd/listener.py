from telethon import events
from telegramProd.message_handler import process_new_message
from config import TELEGRAM_TARGET_CHATS

def register_listener(client, pipeline):

    @client.on(events.NewMessage())
    async def new_message(event):
        # 1️⃣ Filter Sumber Chat
        if event.is_private:
            pass
        elif event.chat_id in TELEGRAM_TARGET_CHATS:
            pass
        else:
            return

        # 2️⃣ Proses standarisasi pesan dan unduh media di latar belakang
        message = await process_new_message(event)
        
        # 3️⃣ Cetak log ringkas penanda pesan masuk ke terminal
        print(f"📥 [Telegram] Pesan baru ({message.message.type}) diterima dari chat: {message.chat.name}")

        # 4️⃣ Alirkan ke pipeline (Database -> Translator -> Formatter -> WhatsApp)
        await pipeline.process(message)