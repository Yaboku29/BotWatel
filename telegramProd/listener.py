from telethon import events

from telegramProd.message_handler import process_new_message


def register_listener(client, pipeline):

    @client.on(events.NewMessage())
    async def new_message(event):

        message = await process_new_message(event)

        await pipeline.process(message)