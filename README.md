# 🛠️ MICROLab Editor v1.0.3

MICROLab web sitesi için geliştirilmiş, bağımsız (standalone), görsel ve modern masaüstü içerik yönetim editörü (Python / Tkinter).

Bu araç sayesinde herhangi bir HTML kodlaması yapmadan; araştırma projeleri, ekip üyesi profilleri, duyurular ve akademik yayınlar hazırlayabilir, tarayıcınızda canlı önizleme yapabilir ve tek tıkla web sitesine uygun içerikler üretebilirsiniz.

---

## 📋 İçindekiler
- [🌟 Öne Çıkan Özellikler](#-öne-çıkan-özellikler)
- [🆕 v1.0.3 ile Gelen Yenilikler](#-v103-ile-gelen-yenilikler)
- [🚀 Kurulum ve Çalıştırma Rehberi](#-kurulum-ve-çalıştırma-rehberi)
  - [💻 Windows İçin](#-windows-için)
  - [🐧 Linux İçin](#-linux-için)
  - [🍎 macOS İçin](#-macos-için)
- [💡 Nasıl Kullanılır? (İçerik Üretim İş Akışı)](#-nasıl-kullanılır-içerik-üretim-iş-akışı)
- [🔄 Otomatik Güncelleme](#-otomatik-güncelleme)
- [❓ Sık Karşılaşılan Sorular ve Çözümleri (FAQ)](#-sık-karşılaşılan-sorular-ve-çözümleri-faq)

---

## 🌟 Öne Çıkan Özellikler

* **4 Modüler İçerik Editörü:**
  * 🚀 **Proje Editörü:** Blok tabanlı sayfa üretici (Başlık, Zengin Metin, Resim Galerisi, YouTube Video Yerleştirici, İstatistik Kartları, İlgili Yayınlar).
  * 👤 **Ekip Üyesi Editörü:** Biyografi, unvan, profil fotoğrafı, araştırma alanları ve resmi SVG logolu akademik linkler (Google Scholar, ORCID, GitHub, LinkedIn vb.).
  * 📰 **Haber Editörü:** Laboratuvar duyuruları, etkinlikler ve gelişme bültenleri.
  * 📚 **Yayın Editörü:** Makale, bildiri ve tezler için DOI/PDF bağlantıları ve yazar bilgileri.
* **Akıllı Canlı Önizleme (Smart Live Preview):** 
  * Tarayıcınızda içerik düzenlerken anlık canlı önizleme.
  * Sayfa yalnızca siz metin veya görsel değiştirdiğinizde yenilenir; gereksiz ekran yanıp sönmeleri (flicker) yaşanmaz ve okuma konumunuz kaybolmaz.
  * İsteğe bağlı olarak "Otomatik Önizleme Yenile" kutusu kapatılarak önizleme duraklatılabilir.
* **Bağımsız ve Taşınabilir:** Herhangi bir kurulum paketi veya ek sunucu gerektirmeden doğrudan Python ile Windows, Linux ve macOS üzerinde çalışır.
* **Akıllı Medya Yönetimi:** Başka bir bilgisayarda üretilmiş veya taşınmış projeler açıldığında fotoğraflar kaybolmaz, sistem tarafından otomatik olarak bağlanır.

---

## 🆕 v1.0.3 ile Gelen Yenilikler

* **macOS Canlı Önizleme Görsel Desteği:** macOS Safari ve Chrome'un katı yerel dosya kısıtlamalarını (`file://` çapraz dizin engeli) aşmak için canlı önizlemede görseller anlık Data URI (base64) motoru ile yüklenir; Finder üzerinden eklenen tüm fotoğraflar önizlemede anında ve eksiksiz görünür.
* **%100 Bağımsız ve Tek Başına Çalışma:** Medya taşınabilirliği, URL güvenliği ve akıllı önizleme motorlarının tamamı doğrudan `app.py` içerisine gömüldü. Dosya Mac veya Linux'a tek başına aktarılsa dahi eksik modül hatası vermeden çalışır.
* **macOS ve Linux Görsel Seçimi:** Mac Finder ve Linux dosya yöneticilerinde fotoğrafların görünmesini engelleyen filtre sorunu giderildi; büyük harfli (`.JPG`, `.PNG`) ve modern formatlar dahil edildi.
* **Akıllı Canlı Önizleme:** Tarayıcı yenilemesi içerik takip motoruna bağlandı. Sayfada değişiklik yokken gereksiz yenilemeler engellendi. "Otomatik Yenile" kapatıldığında tarayıcı yenilemesi anında durur.
* **Proje Taşınabilirliği:** Farklı bilgisayarlardan alınan projeler editöre aktarıldığında kapak fotoğrafları ve galeri görselleri eksiksiz olarak açılır.
* **Güvenli Dosya Kaydı:** Aynı isimde farklı fotoğraflar yüklendiğinde eski fotoğrafların üzerine yazılması önlendi; içerikler çakışmasız olarak saklanır.

---

## 🚀 Kurulum ve Çalıştırma Rehberi

### 💻 Windows İçin

#### Yöntem 1: Tek Tıkla Başlatma (Önerilen)
`project_creator` klasörünün içindeki **`baslat.bat`** dosyasına çift tıklayın. Gerekli kütüphaneler otomatik kontrol edilir ve editör açılır.

#### Yöntem 2: Manuel Başlatma
1. `project_creator` klasöründe terminal veya PowerShell açın.
2. Gereksinimleri yükleyin:
   ```cmd
   python -m pip install -r requirements.txt
   ```
3. Uygulamayı başlatın:
   ```cmd
   python app.py
   ```

---

### 🐧 Linux İçin (Ubuntu, Debian, Fedora, Arch)

#### Yöntem 1: Başlatıcı Script ile (Önerilen)
1. Terminalde `project_creator` klasörüne geçin:
   ```bash
   cd project_creator
   ```
2. Başlatıcıyı çalıştırın:
   ```bash
   chmod +x baslat.sh
   ./baslat.sh
   ```

#### Yöntem 2: Manuel Başlatma
Linux dağıtımınızda grafik arayüz (Tkinter) kütüphanesini yükleyin:
* **Ubuntu / Debian / Linux Mint:**
  ```bash
  sudo apt update && sudo apt install -y python3 python3-pip python3-tk python3-venv
  ```
* **Fedora / RHEL:**
  ```bash
  sudo dnf install -y python3 python3-tkinter
  ```
* **Arch Linux:**
  ```bash
  sudo pacman -S --noconfirm python tk
  ```

Ardından uygulamayı başlatın:
```bash
python3 -m pip install -r requirements.txt
python3 app.py
```

---

### 🍎 macOS İçin

1. Terminal uygulamasını açın ve `project_creator` klasörüne geçin:
   ```bash
   cd /projenin/bulundugu/klasor/project_creator
   ```
2. Başlatıcıyı çalıştırın:
   ```bash
   chmod +x baslat.sh
   ./baslat.sh
   ```
*(Homebrew kullanıyorsanız ve Tkinter uyarısı alırsanız: `brew install python-tk` komutunu çalıştırabilirsiniz).*

---

## 💡 Nasıl Kullanılır? (İçerik Üretim İş Akışı)

1. **İçerik Türünü Seçin:** Üst sekmelerden üretmek istediğiniz alanı (🚀 Proje, 👤 Ekip, 📰 Haber, 📚 Yayın) seçin.
2. **Bilgileri Doldurun:** Başlık, özet, yazar, tarih ve metin alanlarını doldurun.
3. **Bloklar Ekleyin (Projeler İçin):** İhtiyacınıza göre metin, resim, YouTube videosu veya görsel galerisi ekleyip sıralarını kolayca değiştirin.
4. **Canlı Önizleme:** Sağ üst paneldeki **"🌐 Canlı Önizleme"** butonuna basarak sayfanın web sitesinde nasıl görüneceğini tarayıcınızda canlı olarak inceleyin.
5. **Kaydedin:** **"💾 Kaydet"** butonuna basın. Editör, yanında bulunan `website/` klasörünü otomatik olarak algılar ve dosyaları doğrudan site yapısına uygun şekilde kaydeder.

---

## 🔄 Otomatik Güncelleme

Editör, yeni bir sürüm çıktığında bunu otomatik olarak algılar:
* Editör açıldığında yeni bir sürüm olup olmadığı arka planda kontrol edilir.
* Dilerseniz üst menü çubuğundaki **"🔄 Güncelleme Kontrolü"** butonuna basarak dilediğiniz an manuel denetim yapabilirsiniz.
* Yeni bir sürüm bulunduğunda ekranda sürüm notları gösterilir ve tek tıkla güncelleme tamamlanır.

---

## ❓ Sık Karşılaşılan Sorular ve Çözümleri (FAQ)

### 1. Linux'ta `No module named '_tkinter'` Hatası Alıyorum
* **Çözüm:** Dağıtımınıza uygun komutla Tkinter paketini yükleyin:
  * Ubuntu / Debian: `sudo apt install -y python3-tk`
  * Fedora: `sudo dnf install -y python3-tkinter`
  * Arch: `sudo pacman -S tk`

### 2. Önizleme Sayfasında Eski İçerik Görünüyor
* **Çözüm:** Daha önce açık kalmış eski tarayıcı sekmelerini kapatın ve editörden tekrar **"🌐 Canlı Önizleme"** butonuna basın. Yeni önizleme sekmeleri akıllı yenileme altyapısıyla otomatik senkronize olacaktır.

### 3. macOS'ta `Permission denied: ./baslat.sh` Uyarısı Alıyorum
* **Çözüm:** Terminalde `chmod +x baslat.sh` komutunu çalıştırıp izni tanımladıktan sonra tekrar `./baslat.sh` yazarak başlatabilirsiniz.
