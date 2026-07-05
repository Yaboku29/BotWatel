@echo off
title BotWatel Launcher
cls
echo ==================================================
echo           BOTWATEL AUTOMATED LAUNCHER            
echo ==================================================
echo.
echo [1/2] Menyalakan WhatsApp Server di jendela baru...
start "BotWatel - WhatsApp Service" powershell -NoExit -Command "node whatsappProd/server.js"

echo [2/2] Mengaktifkan Venv dan Telegram Engine di jendela baru...
start "BotWatel - Telegram Service" powershell -NoExit -Command "venv\Scripts\activate; python app.py"
echo.
echo ==================================================
echo Sukses! Kedua layanan telah berjalan di luar.
echo Anda bisa menutup atau memakai terminal VSCode ini.
echo ==================================================