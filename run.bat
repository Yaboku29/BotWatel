@echo off
title BotWatel Launcher
cls
echo ==================================================
echo           BOTWATEL AUTOMATED LAUNCHER            
echo ==================================================
echo.

:: 1. PENGECEKAN DEPENDENSI NODE.JS
echo [Check] Memeriksa modul WhatsApp (Node.js)...
if not exist "whatsappProd\node_modules\" (
    echo [!] Folder node_modules tidak ditemukan.
    echo [⚙️] Menjalankan 'npm install' otomatis untuk layanan WhatsApp...
    cd whatsappProd
    call npm install
    cd ..
    echo [✓] Instalasi dependensi Node.js selesai!
) else (
    echo [✓] Modul WhatsApp sudah siap.
)
echo.

:: 2. PENGECEKAN VIRTUAL ENVIRONMENT (VENV) PYTHON
echo [Check] Memeriksa Virtual Environment Python (venv)...
if not exist "venv\" (
    echo [!] Folder venv tidak ditemukan.
    echo [⚙️] Membuat virtual environment baru...
    python -m venv venv
    echo [⚙️] Mengaktifkan venv dan menginstal library dari requirements.txt...
    call venv\Scripts\activate
    pip install -r requirements.txt
    echo [✓] Pembuatan venv dan instalasi library Python selesai!
) else (
    echo [✓] Virtual environment Python sudah siap.
)
echo.
echo ==================================================
echo              MENYALAKAN BOTWATEL                 
echo ==================================================
echo.

echo [1/2] Menyalakan WhatsApp Server di jendela baru...
start "BotWatel - WhatsApp Service" powershell -NoExit -Command "node whatsappProd/server.js"

echo [2/2] Mengaktifkan Venv dan Telegram Engine di jendela baru...
start "BotWatel - Telegram Service" powershell -NoExit -Command "venv\Scripts\activate; python app.py"
echo.
echo ==================================================
echo 🎉 Sukses! Kedua layanan telah berjalan di luar.
echo Anda bisa menutup atau memakai terminal VSCode ini.
echo ==================================================