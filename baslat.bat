@echo off
chcp 65001 >nul
title MICROLab Editor - Başlatıcı
cd /d "%~dp0"

echo ========================================================
echo   MICROLab Editor v1.0.3
echo ========================================================
echo.

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [HATA] Sisteminizde Python bulunamadı!
    echo Lütfen https://www.python.org adresinden Python'u indirip kurun.
    echo (Kurulum ekranında "Add python.exe to PATH" seçeneğini işaretleyin.)
    echo.
    pause
    exit /b 1
)

:: Pillow kontrolü
python -c "import PIL" >nul 2>nul
if %errorlevel% neq 0 (
    echo [BİLGİ] Gerekli görsel eklentileri (Pillow) kuruluyor, lütfen bekleyin...
    python -m pip install -r requirements.txt --quiet
)

echo [OK] Uygulama başlatılıyor...
start "" python app.py
exit
