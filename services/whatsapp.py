from whatsappProd.sender import (
    send_text,
    send_image,
    send_video,
    send_document
)

from config import WA_TARGET_NUMBER

TARGET_NUMBER = WA_TARGET_NUMBER


async def process(message):

    message_info = message.message

    if message_info.type == "Text":

        send_text(
            TARGET_NUMBER,
            message_info.text
        )

    elif message_info.type == "Photo":

        if message_info.file_path is None:
            return

        send_image(
            TARGET_NUMBER,
            str(message_info.file_path),
            message_info.text
        )

    elif message_info.type == "Video":

        if message_info.file_path is None:
            return

        send_video(
            TARGET_NUMBER,
            str(message_info.file_path),
            message_info.text
        )

    elif message_info.type == "Document":

        if message_info.file_path is None:
            return

        send_document(
            TARGET_NUMBER,
            str(message_info.file_path)
        )