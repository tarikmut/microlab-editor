#!/usr/bin/env bash
# MICROLab Editor v1.0.2 - Güvenli Linux/macOS Başlatıcı
set -e
cd "$(dirname "$0")"

echo "========================================================"
echo "  MICROLab Editor v1.0.2"
echo "========================================================"
echo ""

# 1. Python3 Kontrolü
if ! command -v python3 &> /dev/null; then
    echo "[HATA] Sistemde 'python3' bulunamadı!"
    echo "Ubuntu/Debian için: sudo apt update && sudo apt install python3 python3-pip python3-tk python3-venv"
    echo "Fedora için:        sudo dnf install python3 python3-tkinter"
    echo "Arch Linux için:    sudo pacman -S python tk"
    echo "macOS için:         brew install python"
    exit 1
fi

# 2. Tkinter Kontrolü (Linux'ta sistem paketi olarak gereklidir)
if ! python3 -c "import tkinter" &> /dev/null; then
    echo "[HATA] Python Tkinter grafik arayüz modülü sisteminizde yüklü değil!"
    echo "Uygulamanın açılabilmesi için lütfen dağıtımınıza uygun komutu çalıştırın:"
    echo "  Ubuntu / Debian / Mint:  sudo apt update && sudo apt install -y python3-tk"
    echo "  Fedora / RHEL:           sudo dnf install -y python3-tkinter"
    echo "  Arch Linux:              sudo pacman -S --noconfirm tk"
    echo "  macOS (Homebrew):        brew install python-tk"
    echo ""
    exit 1
fi

# 3. İzole Sanal Ortam (.venv) ve Paket Yönetimi (PEP 668 Uyumlu)
VENV_DIR=".venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "[BİLGİ] İzole Python sanal ortamı (.venv) oluşturuluyor..."
    python3 -m venv "$VENV_DIR" 2>/dev/null || true
fi

if [ -f "$VENV_DIR/bin/python" ]; then
    PY_BIN="$VENV_DIR/bin/python"
else
    PY_BIN="python3"
fi

if ! "$PY_BIN" -c "import PIL" &> /dev/null; then
    echo "[BİLGİ] Gerekli paketler yükleniyor (requirements.txt)..."
    "$PY_BIN" -m pip install -r requirements.txt || {
        echo "[UYARI] Sanal ortama yükleme başarısız oldu, kullanıcı dizinine yükleniyor..."
        python3 -m pip install -r requirements.txt --user || true
    }
fi

echo "[OK] MICROLab Editor başlatılıyor..."
exec "$PY_BIN" app.py "$@"
