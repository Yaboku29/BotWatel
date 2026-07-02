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

    msg_type = str(message_info.type).lower()

    try:

        if msg_type == "text":

            send_text(
                TARGET_NUMBER,
                message_info.text or ""
            )

        elif msg_type == "photo":

            if not message_info.file_path:
                return

            send_image(
                TARGET_NUMBER,
                str(message_info.file_path),
                message_info.text or ""
            )

        elif msg_type == "video":

            if not message_info.file_path:
                return

            send_video(
                TARGET_NUMBER,
                str(message_info.file_path),
                message_info.text or ""
            )

        elif msg_type == "document":

            if not message_info.file_path:
                return

            send_document(
                TARGET_NUMBER,
                str(message_info.file_path)
            )

        else:
            print("Unsupported type:", message_info.type)

    except Exception as e:
        print("WhatsApp send error:", e)