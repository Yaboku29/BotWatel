from telegramProd.client import client
from telegramProd.listener import register_listener

from pipeline.pipeline import MessagePipeline

from services.logger import logger_service
from services.whatsapp import process
from services.database import database_service


async def main():

    pipeline = MessagePipeline()

    pipeline.register(logger_service)
    pipeline.register(database_service)
    pipeline.register(process)

    register_listener(client, pipeline)

    me = await client.get_me()

    print(f"Login sebagai : {me.first_name}")
    print("Bot sedang mendengarkan pesan...")

    # async for dialog in client.iter_dialogs():

    #     if "..." in dialog.name:
    #         print("==========================")
    #         print("Nama    :", dialog.name)
    #         print("Chat ID :", dialog.id)
    #         print("Entity  :", type(dialog.entity).__name__)

    await client.run_until_disconnected()


with client:
    client.loop.run_until_complete(main())