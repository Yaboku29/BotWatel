from pathlib import Path
from datetime import datetime
import re

DOWNLOAD_DIR = Path("downloads")


def sanitize_folder_name(name: str):
    if not name:
        name = "Unknown"

    name = re.sub(r'[\\/:*?"<>|]', "_", name)
    return name.strip()


async def download_media(event):
    if not event.message.media:
        return None

    chat = await event.get_chat()

    chat_name = getattr(chat, "title", None) or getattr(chat, "first_name", "Unknown")
    chat_name = sanitize_folder_name(chat_name)

    now = datetime.now()

    save_folder = (
        DOWNLOAD_DIR /
        chat_name /
        str(now.year) /
        f"{now.month:02d}" /
        f"{now.day:02d}"
    )

    save_folder.mkdir(parents=True, exist_ok=True)

    file_path = await event.download_media(file=save_folder)

    if not file_path:
        return None

    # 🔥 PENTING: absolute path
    return str(Path(file_path).resolve())