from pathlib import Path
from datetime import datetime
import re

DOWNLOAD_DIR = Path("downloads")

def sanitize_folder_name(name: str):
    # """
    # Menghapus karakter yang tidak boleh 
    # digunakan sebagai nama folder di Windows
    # """
    if not name:
        name = "Unknown"
    name = re.sub(r'[\\/:*?"<>|]',"_",name)
    return name.strip()


async def download_media(event):
    if not event.message.media:
        return None
    # ambil chat
    chat = await event.get_chat()
    
    # Nama grup/chat
    chat_name=getattr(chat,"title",None) or getattr(chat,"first_name","Unknown")

    # Bersihkan nama folder
    chat_name=sanitize_folder_name(chat_name)

    # Ambil tanggal
    now = datetime.now()

    year=str(now.year)
    month=f"{now.month:02d}"
    day=f"{now.day:02d}"

    # Membuat folder
    save_folder=(
        DOWNLOAD_DIR
        / chat_name
        / year
        / month
        / day
    )

    save_folder.mkdir(parents=True,exist_ok=True)

    # Download Media
    file_path= await event.download_media(file=save_folder)

    return file_path