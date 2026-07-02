# BotWatel

BotWatel adalah aplikasi bridge antara **Telegram** dan **WhatsApp** yang menggunakan akun pribadi (bukan Bot API).

Saat ini BotWatel mampu:

- Login menggunakan akun Telegram melalui Telethon.
- Memonitor pesan Telegram secara realtime.
- Mengunduh media yang diterima.
- Menjalankan koneksi WhatsApp menggunakan Baileys.
- Mengirim pesan teks ke WhatsApp melalui REST API.

Project ini dirancang agar nantinya menjadi **Telegram ↔ WhatsApp Bridge** yang dapat melakukan sinkronisasi pesan dua arah.

---

# Arsitektur

```
                Telegram
                    │
                    ▼
          Telethon (Python)
                    │
                    ▼
            HTTP REST API
                    │
                    ▼
       Express + Baileys (Node.js)
                    │
                    ▼
                WhatsApp
```


Alur kerja:
1. Telegram menerima pesan
2. Python (Telethon) memproses dan mendownload media
3. Python mengirim data ke REST API Node.js
4. Node.js meneruskan ke WhatsApp via Baileys

---

# 🚀 Fitur

## 📩 Telegram (Python - Telethon)

- Login menggunakan akun Telegram pribadi
- Listener pesan realtime
- Mendapatkan metadata pesan:
  - Nama chat
  - Pengirim
  - Username
  - Message type
  - Waktu pesan
- Download media otomatis
- Struktur penyimpanan rapi:
  - Nama Chat
  - Tahun / Bulan / Tanggal
- Support:
  - Text
  - Photo
  - Video
  - Document

---

## 📱 WhatsApp (Node.js - Baileys)

- Login via QR Code
- REST API menggunakan Express
- Kirim pesan:
  - Text
  - Image (file lokal)
  - Video (file lokal)
  - Document (file lokal)
- Auto reconnect socket
- Session persistent (`sessions/`)
- Logging koneksi

---

## 🔗 Bridge System

- Telegram → WhatsApp forwarding
- Kirim text dari Telegram ke WhatsApp
- Kirim media Telegram ke WhatsApp
- File lokal hasil download langsung dikirim ke WhatsApp

---

# 📁 Struktur Project

```text
BotWatel/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
│
├── database/
│   └── database.py
│
├── formatter/
│   ├── __init__.py
│   └── telegram_formatter.py
│
├── models/
│   ├── message.py
│   └── outgoing_message.py
│
├── pipeline/
│   └── pipeline.py
│
├── services/
│   ├── database.py
│   ├── logger.py
│   └── whatsapp.py
│
├── telegramProd/
│   ├── __init__.py
│   ├── client.py
│   ├── downloader.py
│   ├── listener.py
│   └── message_handler.py
│
├── tests/
│   ├── test_api.py
│   └── test_wa.py
│
├── utils/
│
├── whatsappProd/
│   ├── client.js
│   ├── package.json
│   ├── package-lock.json
│   ├── sender.py
│   ├── server.js
│   └── sessions/
│
├── downloads/
│
└── logs/
```
---

# Teknologi yang Digunakan
Python
- Telethon
- Requests
- python-dotenv

Node.js
- Express
- Baileys
- Pino
- qrcode-terminal

---

# ⚙️ Instalasi

## 1. Clone Repository

```bash
git clone https://github.com/username/BotWatel.git
cd BotWatel
```
## 2. Setup Python Environment
```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
```
Install depedency
```bash
pip install -r requirements.txt
```
## 3. Setup Node.js (Whatsapp Service)
Masuk folder:
```bash
cd whatsappProd
```
Install depedency
```bash
npm install
```
## Konfigurasi Telegram
buat file .env:
```env
API_ID=12345678
API_HASH=xxxxxxxxxxxxxxxxxxxx 
```
Dapatkan dari:
https://my.telegram.org/

---

# Cara Menjalankan
## 1. Jalankan Whatsapp Service
```bash
cd whatsappProd
node server.js
```
Scan QR Code:
```
Whatsapp -> Perangkat Tertaut -> Tautkan Perangkat
```
Session akan tersimpan di:
```
whatsappProd/sessions/
```
## 2. Jalankan Telegram Listener
Gunakan terminal yang berbeda dan jalankan:
```bash
python app.py
```
Login Telegram:
- Nomor HP
- OTP Code
- Password (Jika 2FA aktif)

Session tersimpan:
```
watel.session
```

---


# Download Media

Media Telegram akan disimpan dengan struktur

```
downloads/

Nama Chat/

└── Tahun/

    └── Bulan/

        └── Tanggal/

            ├── photo.jpg

            ├── video.mp4

            └── document.pdf
```

---

# REST API

## Mengirim Pesan/Endpoint

```
POST /send
```

## Text Message

```json
{
  "number": "628123456789",
  "type": "text",
  "text": "Halo dari BotWatel"
}
```

## Image Message (Local File)
```json
{
  "number": "628123456789",
  "type": "image",
  "path": "C:/BotWatel/downloads/photo.jpg",
  "caption": "dari Telegram"
}
```

## Response

```json
{
  "success": true,
  "status": "queued"
}
```
---

# Roadmap

## Telegram

- [x] Login
- [x] Listener
- [x] Download Media

## WhatsApp

- [x] Login
- [x] REST API
- [x] Send Text

## Bridge

- [x] Telegram → WhatsApp (Text)
- [x] Telegram → WhatsApp (Photo)
- [x] Telegram → WhatsApp (Video)
- [x] Telegram → WhatsApp (Document)
- [x] Telegram → WhatsApp (Voice)
- [x] Telegram → WhatsApp (GIF)

## Future

- [ ] WhatsApp → Telegram
- [ ] SQLite Database
- [ ] Logging
- [ ] GUI Dashboard
- [ ] Docker Support

---

# Catatan

Project ini menggunakan **akun pribadi Telegram** dan **akun pribadi WhatsApp**.

BotWatel **bukan** menggunakan Telegram Bot API maupun WhatsApp Cloud API.

Koneksi WhatsApp menggunakan **Baileys**, sehingga perubahan pada protokol WhatsApp sewaktu-waktu dapat memengaruhi proses login maupun pengiriman pesan.