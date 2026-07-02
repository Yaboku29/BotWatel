from telethon import events

from telegramProd.message_handler import process_new_message
from whatsappProd.sender import send
from telegramProd.downloader import download_media
from config import TELEGRAM_TARGET_CHATS


def register_listener(client, pipeline):

    @client.on(events.NewMessage())
    async def new_message(event):

        print("Pesan diterima")
        # Selalu izinkan DM
        if event.is_private:
            pass

        # Izinkan group/channel yang ada di konfigurasi
        elif event.chat_id in TELEGRAM_TARGET_CHATS:
            pass

        # Selain itu abaikan
        else:
            return
        # print(f"event.out = {event.out}")
        # print(f"event.is_private = {event.is_private}")

        # if event.out:
        #     print("Keluar karena event.out")
        #     return

        # if not event.is_private:
        #     print("Keluar karena bukan private")
        #     return
        # chat = await event.get_chat()
        # title = getattr(chat, "title", None)

        # if title != "Seele Leaks":
        #     return

        # print("================================")
        # print("Title      :", title)
        # print("Chat ID    :", event.chat_id)
        # print("Is Group   :", event.is_group)
        # print("Is Channel :", event.is_channel)
        # print("================================")

        print(event.raw_text)

        # send_text(
        #     "6285877507211",
        #     event.raw_text
        # )
        message = await process_new_message(event)
        # await download_media(event)
        print(f"[Listener] {message.message.type} diterima")

        await pipeline.process(message)

        print("[Listener] Pipeline selesai")
        print("Pesan dikirim ke API")