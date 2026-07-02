from telethon import events

from telegramProd.message_handler import process_new_message
from whatsappProd.sender import send_text


def register_listener(client, pipeline):

    @client.on(events.NewMessage())
    async def new_message(event):

        print("Pesan diterima")
        
        print(f"event.out = {event.out}")
        print(f"event.is_private = {event.is_private}")

        # if event.out:
        #     print("Keluar karena event.out")
        #     return

        # if not event.is_private:
        #     print("Keluar karena bukan private")
        #     return

        print(event.raw_text)

        send_text(
            "6285877507211",
            event.raw_text
        )

        print("Pesan dikirim ke API")