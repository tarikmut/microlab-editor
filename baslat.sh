#!/usr/bin/env bash
# MICROLab Editor - Linux/macOS Başlatıcı
cd "$(dirname "$0")"

echo "========================================================"
echo "  MICROLab Editor v1.0"
echo "========================================================"
echo ""

# 1. Python3 Kontrolü
if ! command -v python3 &> /dev/null; then
    echo "[HATA] Sistemde 'python3' bulunamadı!"
    echo "Ubuntu/Debian için: sudo apt update && sudo apt install python3 python3-pip python3-tk"
    echo "Fedora için:        sudo dnf install python3 python3-tkinter"
    echo "Arch Linux için:    sudo pacman -S python tk"
    echo "macOS için:         brew install python"
    read -p "Devam etmek için Enter'a basın..."
    exit 1
fi

# 2. Tkinter Kontrolü (Linux'ta bazen ayrı paket olarak gerekir)
if ! python3 -c "import tkinter" &> /dev/null; then
    echo "[UYARI] Python Tkinter grafik arayüz modülü bulunamadı!"
    echo "Lütfen dağıtımınıza uygun komutla tkinter'ı yükleyin:"
    echo "  Ubuntu / Debian / Mint:  sudo apt install python3-tk"
    echo "  Fedora / RHEL:           sudo dnf install python3-tkinter"
    echo "  Arch Linux:              sudo pacman -S tk"
    echo ""
    read -p "Yükledikten sonra devam etmek için Enter'a basın..."
fi

# 3. Pillow Kontrolü
if ! python3 -c "import PIL" &> /dev/null; then
    echo "[BİLGİ] Gerekli eklentiler (Pillow) yükleniyor..."
    python3 -m pip install -r requirements.txt --quiet --user 2>/dev/null || \
    python3 -m pip install -r requirements.txt --quiet --break-system-packages 2>/dev/null || \
    pip install -r requirements.txt --quiet 2>/dev/null || true
fi

echo "[OK] Uygulama başlatılıyor..."
python3 app.py "$@"
