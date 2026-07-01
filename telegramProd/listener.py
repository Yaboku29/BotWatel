from telethon import events
from telegramProd.client import client
from telegramProd.downloader import download_media

def get_message_type(message):
    if message.photo:
        return "Photo"
    if message.video:
        return "Video"
    if message.document:
        return "Document"
    if message.voice:
        return "Voice"
    if message.audio:
        return "Audio"
    if message.sticker:
        return "Sticker"
    if message.gif:
        return "GIF"
    return "Text"

@client.on(events.NewMessage())
async def new_message(event):
    # print("="*50)
    # print("pesan baru diterima!")
    # print(event.raw_text)
    # print("="*50)

    chat = await event.get_chat()
    sender = await event.get_sender()
    message_type = get_message_type(event.message)
    file_path=None

    if event.message.media:
        file_path=await download_media(event)
    
    print("="*60)

    print(f"Chat Name       : {getattr(chat,'title',None) or getattr(chat,'first_name','Unknown')}")
    print(f"Chat ID         : {event.chat_id}")

    print()

    print(f"Sender          : {sender.first_name}")

    username=getattr(sender,"username",None)

    if username:
        print(f"Username        : @{username}")
    else:
        print(f"Username        : -")
    print()

    print(f"Message ID      : {event.id}")
    print(f"Time ID         : {event.date}")
    print(f"Type            : {message_type}")
    print()

    print("TEXT")

    print(event.raw_text)
    if file_path:
        print()
        print(f"Saved File      : {file_path}")

    print("="*60)