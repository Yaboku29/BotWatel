from telegramProd.client import client
import telegramProd.listener


async def main():

    me = await client.get_me()

    print(f"Login sebagai : {me.first_name}")

    print("Bot sedang mendengarkan pesan...")

    await client.run_until_disconnected()


with client:
    client.loop.run_until_complete(main())