from telethon import events

from telegramProd.message_handler import process_new_message
from whatsappProd.sender import send_text


def register_listener(client, pipeline):

    @client.on(events.NewMessage())
    async def new_message(event):

        print("Pesan diterima")

        if event.out:
            return

        if not event.is_private:
            return

        print(event.raw_text)

        send_text(
            "6285xxxxxxxx",
            event.raw_text
        )

        print("Pesan dikirim ke API")