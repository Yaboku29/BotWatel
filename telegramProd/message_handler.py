from models.message import (
    ChatInfo,
    SenderInfo,
    MessageInfo,
    TelegramMessage,
)

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


async def process_new_message(event):

    chat = await event.get_chat()
    sender = await event.get_sender()

    file_path = None

    if event.message.media:
        file_path = await download_media(event)

    return TelegramMessage(

        chat=ChatInfo(
            id=event.chat_id,
            name=getattr(chat, "title", None)
            or getattr(chat, "first_name", "Unknown")
        ),

        sender=SenderInfo(
            id=sender.id if sender else None,
            name=(
                getattr(sender, "first_name", None)
                or getattr(sender, "title", None)
                or "Unknown"
            ),
            username=getattr(sender, "username", None)
        ),

        message=MessageInfo(
            id=event.id,
            date=event.date,
            type=get_message_type(event.message),
            text=event.raw_text,
            has_media=bool(event.message.media),
            file_path=file_path
        )
    )