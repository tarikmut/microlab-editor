# 🛠️ MICROLab Editor v1.0

MICROLab web sitesi için geliştirilmiş, bağımsız (standalone), görsel ve modern masaüstü içerik yönetim editörü (Python / Tkinter). 

Bu araç, web sitesi için HTML kodlamaya gerek kalmadan; projeler, ekip profilleri, haberler ve akademik yayınlar oluşturmanızı, anlık canlı önizleme yapmanızı ve doğrudan web sitesi yapısına uygun çıktılar üretmenizi sağlar.

---

## 📋 İçindekiler
- [🌟 Öne Çıkan Özellikler](#-öne-çıkan-özellikler)
- [🚀 Adım Adım Kurulum ve Çalıştırma Rehberi](#-adım-adım-kurulum-ve-çalıştırma-rehberi)
  - [🪟 Windows İçin](#-windows-için)
  - [🐧 Linux İçin](#-linux-için)
  - [🍎 macOS İçin](#-macos-için)
- [💡 Nasıl Kullanılır? (İçerik Üretim İş Akışı)](#-nasıl-kullanılır-içerik-üretim-iş-akışı)
- [🔄 Sunucusuz Otomatik Güncelleme Sistemi](#-sunucusuz-otomatik-güncelleme-sistemi)
- [❓ Sık Karşılaşılan Sorunlar ve Çözümleri (FAQ)](#-sık-karşılaşılan-sorunlar-ve-çözümleri-faq)

---

## 🌟 Öne Çıkan Özellikler

* **4 Modüler Editör:**
  * 🚀 **Proje Editörü:** Blok tabanlı sayfa üretici (Başlık, Zengin Metin, Resim Galerisi, YouTube Video Yerleştirici, İstatistik Kartları).
  * 👤 **Ekip Üyesi Editörü:** Biyografi, unvan, fotoğraf, ilgi alanları ve resmi SVG logolu sosyal/akademik linkler (Google Scholar, ORCID, GitHub, LinkedIn vb.).
  * 📰 **Haber Editörü:** Laboratuvar duyuruları, etkinlikler ve gelişme bültenleri.
  * 📚 **Yayın Editörü:** Makale, bildiri ve tezler için DOI/PDF bağlantıları ve yazar bilgileri.
* **Canlı Önizleme (Live Preview):** Web sitesi stilleriyle birebir aynı %100 dahili CSS/JS motoru sayesinde tek tıkla tarayıcınızda canlı önizleme.
* **Çapraz Platform:** Windows, Linux ve macOS üzerinde `.exe` derlemesi gerektirmeden doğrudan Python ile çalışır.
* **Sunucusuz Otomatik Güncelleme:** GitHub Releases API üzerinden yeni sürümleri algılar ve kendini tek tıkla günceller ($0 sunucu maliyeti).

---

## 🚀 Adım Adım Kurulum ve Çalıştırma Rehberi

### 🪟 Windows İçin

#### Yöntem 1: Tek Tıkla Başlatma (En Kolay)
1. `project_creator` klasörünün içindeki **`baslat.bat`** dosyasına çift tıklayın.
2. Betik sisteminizde Python'u arar, eksikse `Pillow` görsel kütüphanesini otomatik yükler ve editörü başlatır.

#### Yöntem 2: Komut Satırı / PowerShell İle Manuel Başlatma
1. Klasör boşluğuna `Shift` basılı tutarak sağ tıklayın ve **"PowerShell penceresini burada aç"** deyin.
2. Python'un kurulu olduğunu doğrulayın:
   ```powershell
   python --version
   ```
   *(Eğer hata alırsanız [python.org](https://www.python.org) adresinden Python 3.8+ indirin. Kurulum sihirbazında **"Add Python to PATH"** seçeneğini işaretleyin).*
3. Gerekli kütüphaneleri yükleyin:
   ```powershell
   python -m pip install -r requirements.txt
   ```
4. Uygulamayı çalıştırın:
   ```powershell
   python app.py
   ```

---

### 🐧 Linux İçin (Ubuntu, Debian, Fedora, Arch)

Linux dağıtımlarında Tkinter genellikle ana Python paketiyle birlikte kurulmaz; bu nedenle ilk kez çalıştırırken Tkinter paketini yüklemek gerekir.

#### Yöntem 1: Başlatıcı Script ile
1. Terminali açın (`Ctrl + Alt + T`).
2. `project_creator` dizinine geçin:
   ```bash
   cd /projenin/bulundugu/dizin/project_creator
   ```
3. Script'e çalıştırma izni verip çalıştırın:
   ```bash
   chmod +x baslat.sh
   ./baslat.sh
   ```

#### Yöntem 2: Manuel Kurulum ve Çalıştırma Adımları
1. **Tkinter Grafik Kütüphanesini Yükleyin:**
   * **Ubuntu / Debian / Linux Mint:**
     ```bash
     sudo apt update && sudo apt install python3 python3-pip python3-tk
     ```
   * **Fedora / RHEL:**
     ```bash
     sudo dnf install python3 python3-tkinter
     ```
   * **Arch Linux / Manjaro:**
     ```bash
     sudo pacman -S python python-pillow tk
     ```
2. **Pillow Kütüphanesini Kurun:**
   ```bash
   pip install -r requirements.txt
   ```
   *(Hata alırsanız: `python3 -m pip install -r requirements.txt --break-system-packages`)*
3. **Uygulamayı Başlatın:**
   ```bash
   python3 app.py
   ```

---

### 🍎 macOS İçin

1. **Terminali Açın:** Spotlight (`Cmd + Space`) ile `Terminal` yazıp açın.
2. **Dizine Geçin:**
   ```bash
   cd /projenin/bulundugu/dizin/project_creator
   ```
3. **Çalıştırma İzni Verin ve Başlatın:**
   ```bash
   chmod +x baslat.sh
   ./baslat.sh
   ```
4. **Manuel Çalıştırmak İsterseniz:**
   ```bash
   pip3 install -r requirements.txt
   python3 app.py
   ```
   *(Homebrew kullanıyorsanız ve Tkinter hatası alırsanız: `brew install python-tk`)*

---

## 💡 Nasıl Kullanılır? (İçerik Üretim İş Akışı)

1. **Sekme Seçin:** Üstteki sekmelerden üretmek istediğiniz içerik türünü (🚀 Proje, 👤 Ekip, 📰 Haber, 📚 Yayın) seçin.
2. **Form Alanlarını Doldurun:** Başlık, özet, yazar, tarih gibi temel bilgileri girin.
3. **Bloklar Ekleyin (Projeler İçin):** İhtiyacınıza göre metin, resim, YouTube videosu veya istatistik kartları ekleyip blokları dilediğiniz gibi düzenleyin.
4. **Canlı Önizleme Yapın:** Sağ paneldeki **"🌐 Canlı Önizleme"** butonuna basarak sayfanın web sitesinde nasıl görüneceğini tarayıcınızda açın.
5. **Kaydet ve Dışa Aktar:**
   * **"💾 Projeyi Kaydet"** butonuna basın.
   * Editör, projenin yanında `website/` klasörü varsa onu otomatik algılar ve çıktıyı doğrudan ilgili `website/projects/data/` klasörüne yazar.
   * Eğer web sitesi klasörü bulunamazsa, kendi içindeki `exports/` klasörüne kaydeder.

---

## 🔄 Sunucusuz Otomatik Güncelleme Sistemi

Uygulama, GitHub Releases API'sini kullanarak kendini tamamen ücretsiz olarak günceller:

* **Açılışta Sessiz Kontrol:** Editör açıldıktan 3.5 saniye sonra arka planda GitHub'a bağlanıp yeni sürüm olup olmadığını kontrol eder.
* **Manuel Kontrol:** Üst başlıktaki **`🔄 Güncelleme Kontrolü`** butonuna basarak istediğiniz an denetleyebilirsiniz.
* **Otomatik Kurulum:** Yeni bir sürüm varsa değişiklik notları ekranda gösterilir. Onay verdiğinizde yeni `app.py` indirilir, eskisinin yedeği (`app.py.bak`) alınır ve uygulama otomatik olarak yeniden başlatılır.

### Yeni Sürüm (Örn: v1.1.0) Yayınlama Rehberi:
1. `app.py` içerisindeki `APP_VERSION = "1.1.0"` değerini güncelleyip GitHub reponuza push edin.
2. GitHub reponuzda **Releases** -> **"Draft a new release"** bölümüne gidin.
3. **Tag version:** `v1.1.0` (veya `v1.1`) yazın.
4. **Release title:** `MICROLab Editor v1.1 Güncellemesi` yazın.
5. Açıklama kutusuna yapılan yenilikleri yazın ve **Publish release** butonuna basın.
6. Tüm kullanıcılar uygulamayı açtığı anda güncelleme otomatik olarak ekranlarına gelecektir.

---

## ❓ Sık Karşılaşılan Sorunlar ve Çözümleri (FAQ)

### 1. `ModuleNotFoundError: No module named '_tkinter'` Hatası
* **Neden:** Linux işletim sisteminde Tkinter dahili olarak kurulu gelmez.
* **Çözüm:** Dağıtımınıza uygun paket yöneticisiyle yükleyin:
  * Ubuntu / Debian: `sudo apt install python3-tk`
  * Fedora: `sudo dnf install python3-tkinter`
  * macOS: `brew install python-tk`

### 2. `ModuleNotFoundError: No module named 'PIL'` Hatası
* **Neden:** Pillow görsel işleme kütüphanesi yüklü değildir.
* **Çözüm:** Terminalde `pip install -r requirements.txt` veya `pip install Pillow` komutunu çalıştırın.

### 3. Linux / Mac'te `Permission denied: ./baslat.sh` Hatası
* **Neden:** Dosyanın çalıştırma (execute) yetkisi verilmemiştir.
* **Çözüm:** Terminalde `chmod +x baslat.sh` komutunu çalıştırıp tekrar `./baslat.sh` deneyin.
