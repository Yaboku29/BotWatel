import os
from pathlib import Path
from whatsappProd.sender import send_text, send_image, send_video, send_document
from config import WA_COMMUNITY_ANNOUNCEMENT_NUMBER
from formatter.telegram_formatter import format_message
# Import fungsi update status
from services.database import is_part_of_album, update_message_status 

TARGET_NUMBER = WA_COMMUNITY_ANNOUNCEMENT_NUMBER

async def process(message):
    try:
        msg_info = message.message
        media_path = msg_info.file_path
        msg_type = str(msg_info.type).lower()

        # 1️⃣ Cek apakah ini bagian dari album (pesan beruntun)
        is_album = is_part_of_album(message.chat.id, threshold_seconds=4)

        # 2️⃣ Tentukan caption
        if is_album:
            caption_to_send = ""
        else:
            formatted_msg = format_message(message)
            caption_to_send = formatted_msg.text

        # 3️⃣ Kirim ke WhatsApp
        if msg_type == "text":
            send_text(TARGET_NUMBER, caption_to_send)

        elif msg_type == "photo":
            if not media_path or not Path(media_path).exists():
                return
            send_image(TARGET_NUMBER, str(media_path), caption=caption_to_send)

        elif msg_type == "video":
            if not media_path or not Path(media_path).exists():
                return
            send_video(TARGET_NUMBER, str(media_path), caption=caption_to_send)

        elif msg_type == "document":
            if not media_path or not Path(media_path).exists():
                return
            send_document(TARGET_NUMBER, str(media_path))
            if not is_album and caption_to_send:
                send_text(TARGET_NUMBER, caption_to_send)

        # 4️⃣ PENTING: Tandai pesan ini sebagai 'PROCESSED' di database agar foto berikutnya tahu ada album
        update_message_status(msg_info.id, message.chat.id, 'PROCESSED')

        # 5️⃣ Auto-Clean
        if media_path and Path(media_path).exists():
            try:
                os.remove(media_path)
                print(f"🗑️ [Auto-Clean] File dihapus: {Path(media_path).name}")
            except Exception as clean_err:
                print(f"⚠️ [Auto-Clean Gagal] {str(clean_err)}")

    except Exception as e:
        print(f"❌ Error pada WhatsApp Service: {str(e)}")