# BotWatel 📨

BotWatel adalah aplikasi bridge (penghubung) otomatis antara **Telegram** dan **WhatsApp** yang memanfaatkan akun pribadi (Userbot). Proyek ini bekerja secara bebas tanpa memerlukan Bot API resmi dari kedua platform tersebut.

Saat ini, sistem diimplementasikan satu arah (**Telegram → WhatsApp**) untuk meneruskan berbagai pesan secara realtime.

---

## ✨ Fitur Utama

- **Userbot Engine:** Berjalan menggunakan akun Telegram pribadi (via Telethon) dan WhatsApp pribadi (via Baileys).
- **Realtime Listener:** Memonitor pesan masuk dari DM (Private Chat), Group, maupun Channel Telegram secara instan.
- **Target Filtering:** Memfilter sumber pesan masuk berdasarkan Chat ID Telegram yang dikonfigurasi pada file `.env`.
- **Auto-Download Media:** Mengunduh media Telegram otomatis (Foto, Video, Dokumen, Voice, Audio, Sticker, GIF) dan menyimpannya ke folder lokal.
- **Pipeline Architecture:** Menggunakan pola desain modular (*Chain of Responsibility*) sehingga mempermudah penambahan layanan baru (Logger, DB, Translator, Formatter).
- **Realtime Translation:** Mendeteksi bahasa asing otomatis dan menerjemahkannya ke bahasa Inggris via Google Translate sebelum dikirim ke WhatsApp.
- **Media Caption:** Mempertahankan teks caption asli pada media (foto/video) saat diteruskan.
- **Non-Blocking REST API:** Mengirim pesan via HTTP POST ke server Node.js dengan sistem antrean latar belakang (*queued*) agar performa Python tetap responsif.

---

## 🏗️ Arsitektur Sistem
```
            Telegram Chat
                  │
                  ▼
          Telethon (Python)
                  │ (HTTP POST JSON)
                  ▼
      Express API + Baileys (Node.js)
                  │
                  ▼
            WhatsApp Chat
```


---

## 📂 Struktur Properti & Folder


```

BotWatel/
├── .env                    # File konfigurasi kredensial & environment variable
├── app.py                  # Entry point utama aplikasi Python
├── config.py               # Pengelola konfigurasi & pemetaan variabel .env
├── requirements.txt        # Daftar dependensi library Python
├── database/               # Folder penyimpanan SQLite database (botwatel.db)
├── downloads/              # Folder penyimpanan media dari Telegram (diatur otomatis)
├── formatter/              # Modul penyusun tampilan teks laporan pesan
│   └── telegram_formatter.py
├── models/                 # Definisi struktur objek data (Dataclasses Python)
│   ├── message.py
│   └── outgoing_message.py
├── pipeline/               # Arsitektur orkestrasi berantai pemrosesan pesan
│   └── pipeline.py
├── services/               # Layanan pipeline (Logger, DB, Translator, WhatsApp Sender)
│   ├── database.py
│   ├── logger.py
│   ├── translator.py
│   └── whatsapp.py
└── whatsappProd/           # Modul WhatsApp (Server Node.js & REST API Driver)
    ├── client.js
    ├── package.json
    ├── sender.py
    └── server.js

```

### Aturan Penyimpanan Media
Media yang diunduh dari Telegram akan otomatis tersimpan dengan struktur folder absolut berbasis nama chat dan waktu:

```

downloads/
└── [Nama Chat]/
└── [Tahun]/
└── [Bulan]/
└── [Tanggal]/
├── photo.jpg
└── video.mp4

```

---

## 🚀 Panduan Instalasi & Penggunaan

Proyek ini membutuhkan pemahaman dasar mengenai penggunaan terminal/command prompt. Pastikan komputer Anda sudah terinstal **Python 3.10+** dan **Node.js 18+**.

### 1. Kloning Repositori
```bash
git clone [https://github.com/username/BotWatel.git](https://github.com/username/BotWatel.git)
cd BotWatel

```

### 2. Konfigurasi Environment (`.env`)

Buat sebuah file baru bernama `.env` di root folder utama proyek `BotWatel/`, lalu sesuaikan nilainya:

```env
# ==========================================
# TELEGRAM CREDENTIALS (my.telegram.org)
# ==========================================
API_ID=12345678
API_HASH=abcdef0123456789abcdef0123456789

# TARGET CHATS (Pisahkan dengan koma jika multi-chat, kosongkan/DM otomatis masuk)
TELEGRAM_TARGET_CHATS=123456789,-100123456789

# ==========================================
# WHATSAPP API & TARGET
# ==========================================
WA_API_URL=http://localhost:3000
WA_TARGET_NUMBER=628123456789
WA_COMMUNITY_ANNOUNCEMENT_NUMBER=628123456789-1600000000@g.us

# ==========================================
# DATABASE & SYSTEM LOG
# ==========================================
DATABASE_PATH=database/botwatel.db
LOG_LEVEL=INFO

```

### 3. Setup Layanan WhatsApp (Node.js)

Buka terminal baru, masuk ke folder modul WhatsApp, pasang dependensi, lalu jalankan servernya:

```bash
cd whatsappProd
npm install
node server.js

```

*Catatan: Saat pertama kali dijalankan, terminal akan merender QR Code kecil. Buka WhatsApp HP Anda -> Perangkat Tertaut -> Scan QR tersebut. Sesi login akan disimpan secara permanen di dalam folder `sessions/`.*

### 4. Setup Layanan Telegram & Core (Python)

Buka terminal baru satu lagi (kembali ke root folder utama `BotWatel`), instal dependensi melalui file `requirements.txt`, lalu jalankan aplikasi utamanya:

```bash
pip install -r requirements.txt
python app.py

```

*Catatan: Pada peluncuran pertama, Telethon di terminal akan meminta Anda memasukkan nomor HP (gunakan format internasional, misal: +628xxx) dan memasukkan kode OTP resmi yang dikirimkan oleh sistem Telegram.*

---

## 🔌 REST API Reference (Node.js Service)

Server Node.js secara default berjalan di `http://localhost:3000` dan mengekspos endpoint HTTP yang ditembak oleh `sender.py` di sisi Python.

### Mengirim Pesan

* **Endpoint:** `POST /send`
* **Headers:** `Content-Type: application/json`

#### Contoh Payload Pesan Teks:

```json
{
  "number": "628123456789",
  "type": "text",
  "text": "Halo dari BotWatel!"
}

```

#### Contoh Payload Pesan Gambar (File Lokal Absolut):

```json
{
  "number": "628123456789",
  "type": "image",
  "path": "C:/BotWatel/downloads/Group_A/2026/07/03/photo.jpg",
  "caption": "Pesan gambar yang diteruskan dari Telegram"
}

```

#### Response (Non-blocking):

```json
{
  "success": true,
  "status": "queued"
}

```

---

## 🗺️ Roadmap Pengembangan

* [x] Login Telegram Userbot (Telethon)
* [x] Listener & Filter Chat ID Telegram
* [x] Auto-Download Media Telegram (Absolute Path & Sanitized Folder)
* [x] Login WhatsApp Userbot (Baileys dengan Auth File State)
* [x] Node.js REST API Server & Integrasi Multi-language (Python ↔ Node.js)
* [x] Modular Message Pipeline Arsitektur
* [x] Realtime Auto Translation (deep-translator)
* [ ] Implementasi Database SQLite nyata pada `database_service`
* [ ] Pengaktifan Modul `telegram_formatter` secara menyeluruh pada alur WhatsApp
* [ ] Sinkronisasi Dua Arah Penuh (WhatsApp ↔ Telegram Bridge)
