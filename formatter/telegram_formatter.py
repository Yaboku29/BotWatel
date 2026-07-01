from pathlib import Path

from models.message import TelegramMessage
from models.outgoing_message import OutgoingMessage


def format_message(message: TelegramMessage) -> OutgoingMessage:

    lines = []

    lines.append("📨 Telegram Forward")

    lines.append("")

    lines.append(f"Chat : {message.chat.name}")

    lines.append(f"Sender : {message.sender.name}")

    if message.sender.username:
        lines.append(f"Username : @{message.sender.username}")

    lines.append(f"Type : {message.message.type}")

    lines.append(f"Time : {message.message.date}")

    if message.message.text:

        lines.append("")

        lines.append(message.message.text)

    return OutgoingMessage(

        text="\n".join(lines),

        media_path=message.message.file_path,

        media_type=message.message.type
    )