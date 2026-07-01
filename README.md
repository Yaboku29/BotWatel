# BotWatel

BotWatel adalah aplikasi Python yang menggunakan **Telethon** untuk memonitor pesan Telegram menggunakan akun pribadi, kemudian menyimpan media yang diterima ke dalam folder lokal. Proyek ini dirancang agar nantinya dapat dikembangkan menjadi **Telegram → WhatsApp Bridge**.

---

## Fitur

- Login menggunakan akun Telegram pribadi
- Menerima seluruh pesan baru secara realtime
- Menampilkan informasi pesan
  - Nama chat
  - Chat ID
  - Pengirim
  - Username
  - Message ID
  - Waktu
  - Jenis pesan
  - Isi pesan
- Mengunduh media secara otomatis
- Menyimpan media berdasarkan:
  - Nama chat
  - Tahun
  - Bulan
  - Tanggal

Contoh struktur folder hasil download:

downloads/
```
Nama Grup/
└── 2026/
└── 07/
└── 01/
├── photo.jpg
├── document.pdf
└── video.mp4
```

---

## Requirement

- Python 3.11+
- Telegram API ID
- Telegram API Hash

---

## Instalasi

### Clone repository

```bash
git clone https://github.com/username/BotWatel.git

cd BotWatel
```

---

### Buat Virtual Environment

Windows

```bash
python -m venv .venv
```

Aktifkan

```bash
.venv\Scripts\activate
```

Linux / Mac

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

### Install dependency

```bash
pip install -r requirements.txt
```

---

## Membuat API Telegram

Masuk ke

https://my.telegram.org

Login menggunakan nomor Telegram.
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

Python bertugas membaca pesan Telegram.

Node.js bertugas mengelola koneksi WhatsApp.

Keduanya saling berkomunikasi melalui HTTP API.

---

# Fitur

## Telegram

- Login menggunakan akun Telegram pribadi
- Mendengarkan pesan secara realtime
- Mengambil informasi pesan
- Download media secara otomatis
- Menyimpan media berdasarkan:
    - Nama Chat
    - Tahun
    - Bulan
    - Tanggal

## WhatsApp

- Login menggunakan akun WhatsApp pribadi
- REST API menggunakan Express
- Mengirim pesan teks ke WhatsApp

---

# Requirement

- Python 3.11+
- Node.js 20+
- Telegram API ID
- Telegram API Hash
- Akun WhatsApp

---

# Instalasi

## Clone Repository

```bash
git clone https://github.com/username/BotWatel.git

cd BotWatel
```

---

## Membuat Virtual Environment

Windows

```bash
python -m venv .venv
```

Aktifkan

```bash
.venv\Scripts\activate
```

Linux / Mac

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## Install Dependency Python

```bash
pip install -r requirements.txt
```

---

## Install Dependency WhatsApp

Masuk ke folder

```bash
cd whatsappProd
```

Kemudian install package Node.js

```bash
npm install
```

---

# Membuat Telegram API

Masuk ke

https://my.telegram.org

Login menggunakan nomor Telegram.

Pilih

```
API Development Tools
```

Kemudian buat aplikasi baru.

Catat:

- API ID
- API Hash

---

# Konfigurasi

Buat file

```
.env
```

Isi dengan

```env
API_ID=12345678
API_HASH=xxxxxxxxxxxxxxxxxxxxxxxx
```

---

# Menjalankan Program

BotWatel terdiri dari dua service.

## 1. Jalankan WhatsApp API

Masuk ke folder

```bash
cd whatsappProd
```

Kemudian jalankan

```bash
node server.js
```

Saat pertama kali dijalankan akan muncul QR Code.

Scan menggunakan

```
WhatsApp
↓

Perangkat Tertaut

↓

Tautkan Perangkat
```

Setelah berhasil login, credential akan disimpan pada folder

```
whatsappProd/sessions/
```

Sehingga tidak perlu scan ulang setiap menjalankan aplikasi.

---

## 2. Jalankan Telegram Listener

Buka terminal baru.

Aktifkan Virtual Environment.

Kemudian jalankan

```bash
python app.py
```

Saat pertama kali dijalankan akan diminta

```
Phone Number
```

Masukkan nomor Telegram.

Kemudian

```
Login Code
```

Jika menggunakan Two-Step Verification

```
Password
```

Setelah berhasil login akan terbentuk file

```
watel.session
```

---

# Struktur Project

```
BotWatel/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
│
├── telegramProd/
│   ├── client.py
│   ├── downloader.py
│   ├── listener.py
│   ├── message_handler.py
│   └── models/
│
├── whatsappProd/
│   ├── client.js
│   ├── server.js
│   ├── sender.py
│   ├── package.json
│   ├── package-lock.json
│   └── sessions/
│
├── downloads/
│
└── logs/
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

## Mengirim Pesan

```
POST /send
```

Body

```json
{
    "number":"628123456789",
    "text":"Halo dari BotWatel"
}
```

Response

```json
{
    "success": true
}
```

---

# Dependency

## Python

- Telethon
- python-dotenv
- requests

Install

```bash
pip install -r requirements.txt
```

---

## Node.js

Install

```bash
npm install
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

- [ ] Telegram → WhatsApp (Text)
- [ ] Telegram → WhatsApp (Photo)
- [ ] Telegram → WhatsApp (Video)
- [ ] Telegram → WhatsApp (Document)
- [ ] Telegram → WhatsApp (Voice)
- [ ] Telegram → WhatsApp (Sticker)

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
Pilih

```
API Development Tools
```

Kemudian buat aplikasi baru.

Catat:

- API ID
- API Hash

---

## Konfigurasi

Buat file

```
.env
```

Isi dengan

```env
API_ID=12345678
API_HASH=xxxxxxxxxxxxxxxxxxxxxxxx
```

---

## Menjalankan Program

```bash
python app.py
```

Saat pertama kali dijalankan akan diminta:

```
Phone Number
```

Masukkan nomor Telegram.

Setelah itu masukkan:

```
Login Code
```

Jika menggunakan Two-Step Verification:

```
Password
```

Setelah berhasil login akan muncul file:

```
watel.session
```

File ini digunakan agar tidak perlu login ulang setiap menjalankan program.

---

## Struktur Project

```
BotWatel/
│
├── app.py
├── .env
├── README.md
├── downloads/
│
└── telegramProd/
    ├── client.py
    ├── downloader.py
    ├── listener.py
```

---

## Output Contoh

```
============================================================

Chat Name : Belajar Python
Chat ID   : -1001234567890

Sender    : Rizky

Username  : @rizky

Message ID : 1234

Time       : 2026-07-01 20:30

Type       : Photo

TEXT

Halo semua

Saved File

downloads/
Belajar Python/
2026/
07/
01/
photo.jpg

============================================================
```

---

## Dependency

```
Telethon
python-dotenv
```

atau install menggunakan

```bash
pip install telethon python-dotenv
```

---

## Roadmap

- [x] Login menggunakan akun Telegram
- [x] Menerima pesan realtime
- [x] Download media
- [ ] Forward pesan ke WhatsApp
- [ ] Auto Reply WhatsApp
- [ ] Database SQLite
- [ ] Logging
- [ ] GUI Dashboard
- [ ] Docker Support