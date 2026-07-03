import os
from pathlib import Path
from whatsappProd.sender import (
    send_text,
    send_image,
    send_video,
    send_document
)

from config import WA_COMMUNITY_ANNOUNCEMENT_NUMBER
# 1️⃣ Import fungsi formatter yang sudah kamu buat sebelumnya
from formatter.telegram_formatter import format_message

TARGET_NUMBER = WA_COMMUNITY_ANNOUNCEMENT_NUMBER

async def process(message):
    try:
        # 2️⃣ Gunakan formatter untuk mengubah TelegramMessage menjadi OutgoingMessage yang rapi
        formatted_msg = format_message(message)
        
        # Ambil data teks hasil format dan informasi medianya
        text_content = formatted_msg.text
        media_path = formatted_msg.media_path
        msg_type = str(formatted_msg.media_type).lower() if formatted_msg.media_type else "text"

        # Hubungkan ke driver pengirim berdasarkan tipe medianya
        if msg_type == "text":
            send_text(
                TARGET_NUMBER,
                text_content
            )

        elif msg_type == "photo":
            if not media_path or not Path(media_path).exists():
                return
            send_image(
                TARGET_NUMBER,
                str(media_path),
                caption=text_content  # Teks laporan otomatis jadi caption gambar
            )

        elif msg_type == "video":
            if not media_path or not Path(media_path).exists():
                return
            send_video(
                TARGET_NUMBER,
                str(media_path),
                caption=text_content  # Teks laporan otomatis jadi caption video
            )

        elif msg_type == "document":
            if not media_path or not Path(media_path).exists():
                return
            # Kirim dokumennya terlebih dahulu
            send_document(
                TARGET_NUMBER,
                str(media_path)
            )
            # Kirim teks laporannya secara terpisah setelah dokumen terkirim
            send_text(
                TARGET_NUMBER,
                text_content
            )

        # 3️⃣ AUTO-CLEAN MEDIA: Hapus file lokal setelah dikirim ke REST API Node.js
        if media_path and Path(media_path).exists():
            try:
                os.remove(media_path)
                print(f"🗑️ [Auto-Clean] Berhasil menghapus file lokal: {media_path}")
            except Exception as clean_err:
                print(f"⚠️ [Auto-Clean] Gagal menghapus file: {str(clean_err)}")

    except Exception as e:
        print(f"❌ Error pada layanan WhatsApp Service: {str(e)}")