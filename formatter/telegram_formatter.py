from pathlib import Path
from models.message import TelegramMessage
from models.outgoing_message import OutgoingMessage

def format_message(message: TelegramMessage) -> OutgoingMessage:
    lines = []
    
    # Header Laporan Forwarding
    lines.append("📨 *TELEGRAM FORWARD*")
    # lines.append(f"• *Chat:* {message.chat.name}")
    lines.append(f"• *Sender:* {message.sender.name}")
    
    if message.sender.username:
        lines.append(f"• *Username:* @{message.sender.username}")
        
    lines.append(f"• *Type:* {message.message.type}")
    
    # Format waktu agar lebih manusiawi (Jam:Menit)
    try:
        formatted_time = message.message.date.strftime("%Y-%m-%d %H:%M:%S")
    except AttributeError:
        formatted_time = str(message.message.date)
        
    lines.append(f"• *Time:* {formatted_time}")
    lines.append("=" * 30) # Pembatas horizontal ramping

    # Jika ada isi teks (atau teks hasil terjemahan dari translator_service)
    if message.message.text:
        lines.append(message.message.text)

    return OutgoingMessage(
        text="\n".join(lines),
        media_path=message.message.file_path,
        media_type=message.message.type
    )