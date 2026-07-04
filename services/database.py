import sqlite3
from pathlib import Path
from datetime import datetime 
from config import DATABASE_PATH

def init_db():
    db_file = Path(DATABASE_PATH)
    db_file.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS message_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_msg_id INTEGER,
            chat_id INTEGER,
            chat_name TEXT,
            sender_name TEXT,
            message_type TEXT,
            timestamp TEXT,
            status TEXT DEFAULT 'PENDING'
        )
    """)
    conn.commit()
    conn.close()

init_db()

def is_part_of_album(chat_id: int, threshold_seconds: int = 4) -> bool:
    """Mengecek album HANYA pada pesan yang sudah sukses diproses sebelumnya."""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # PENTING: Hanya cari yang statusnya 'PROCESSED'
        cursor.execute("""
            SELECT timestamp FROM message_logs 
            WHERE chat_id = ? AND status = 'PROCESSED'
            ORDER BY id DESC LIMIT 1
        """, (chat_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            last_time = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
            if (datetime.now() - last_time).total_seconds() <= threshold_seconds:
                return True
                
        return False
    except Exception as e:
        print(f"⚠️ [Database Check Album Error] {str(e)}")
        return False

def update_message_status(telegram_msg_id: int, chat_id: int, status: str):
    """Mengubah status pesan menjadi PROCESSED setelah selesai ditangani di whatsapp.py"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE message_logs SET status = ? 
            WHERE telegram_msg_id = ? AND chat_id = ?
        """, (status, telegram_msg_id, chat_id))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"⚠️ [Database Update Error] {str(e)}")

async def database_service(message):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        msg_info = message.message
        chat_info = message.chat
        sender_info = message.sender
        
        formatted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Masuk pertama kali dengan status 'PENDING' agar tidak mengacaukan foto pertama
        cursor.execute("""
            INSERT INTO message_logs (telegram_msg_id, chat_id, chat_name, sender_name, message_type, timestamp, status)
            VALUES (?, ?, ?, ?, ?, ?, 'PENDING')
        """, (
            msg_info.id,
            chat_info.id,
            chat_info.name,
            sender_info.name,
            msg_info.type,
            formatted_time
        ))
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"⚠️ [Database Error] Gagal menyimpan log: {str(e)}")