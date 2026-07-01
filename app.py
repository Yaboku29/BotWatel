from telegramProd.client import client
from telegramProd.listener import register_listener

from pipeline.pipeline import MessagePipeline

from services.logger import logger_service
from services.whatsapp import whatsapp_service
from services.database import database_service


async def main():

    pipeline = MessagePipeline()

    pipeline.register(logger_service)
    pipeline.register(database_service)
    pipeline.register(whatsapp_service)

    register_listener(client, pipeline)

    me = await client.get_me()

    print(f"Login sebagai : {me.first_name}")
    print("Bot sedang mendengarkan pesan...")

    await client.run_until_disconnected()


with client:
    client.loop.run_until_complete(main())