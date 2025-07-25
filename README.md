# 🛒 E-Ticaret Fiyat Karşılaştırma Aracı

Bu araç, popüler e-ticaret sitelerinden anlık fiyat verisi çekerek, aradığınız ürün için en iyi teklifleri bulmanızı sağlar ve sonuçları Excel raporu olarak sunar.

---

## 🌟 Özellikler

- ✅ **Geniş Site Desteği:** Amazon, Çiçeksepeti, Hepsiburada, N11, Temu ve Trendyol  
- 🤖 **Captcha Çözücü:** Sürükle-bırak captcha’ları otomatik olarak çözmeye çalışır  
- 🧍 **Manuel Destek:** Otomasyon başarısız olursa, captcha’yı manuel çözmeniz için size 10 saniye tanır  
- 💬 **Etkileşimli Arayüz:** Komut satırından sizi yönlendirerek kullanım kolaylığı sağlar  
- 🔧 **Esnek Yapılandırma:** Sadece bir dosyadaki ayarlarla site seçimi yapabilirsiniz  

---

## 📂 Proje Yapısı

```plaintext
📦 fiyat-karsilastirma-araci
├── 📜 main.py             # Ana program ve orkestrasyon
├── 🐍 amazon.py           # Amazon için tarama modülü
├── 🐍 ciceksepeti.py      # Çiçeksepeti için tarama modülü
├── 🐍 hepsiburada.py      # Hepsiburada için tarama modülü
├── 🐍 n11.py              # N11 için tarama modülü
├── 🐍 temu.py             # Temu için tarama ve captcha modülü
└── 🐍 trendyol.py         # Trendyol için tarama modülü
```

---

## 🚀 Kurulum Adımları

### 1. Projeyi Klonlayın veya İndirin

Tüm `.py` dosyalarını bir klasöre indirin.

### 2. Gerekli Kütüphaneleri Yükleyin

Terminal veya komut istemcisine şu komutu yazın:

```bash
pip install pandas selenium undetected-chromedriver requests beautifulsoup4 openpyxl
```

> **Not:** Python 3.7+ ve Google Chrome yüklü olmalıdır.

---

## 🏃‍♀️ Nasıl Kullanılır?

1. Terminali açın ve proje klasörüne gidin:
   ```bash
   cd klasor_adi
   python main.py
   ```

2. Program sizden ürün adını ve kaç ürün listeleneceğini isteyecek:
   ```
   Aranacak ürünün adını girin:
   Her siteden kaç ürün listelensin? (Varsayılan: 5):
   ```

3. Araç siteleri taramaya başlayacak. Captcha çıkarsa otomatik çözmeyi deneyecek, olmazsa yardım isteyecek.

4. İşlem sonunda şuna benzer bir Excel dosyası oluşur:

   ```
   FiyatRaporu_Telefon_2025-07-25_14-52.xlsx
   ```

---

## ⚙️ Yapılandırma

`main.py` içinde yer alan `SITES_TO_SCRAPE` sözlüğünden hangi sitelerin taranacağını kolayca kontrol edebilirsiniz:

```python
SITES_TO_SCRAPE = {
    'amazon': True,
    'hepsiburada': False,
    'trendyol': True,
    'n11': False,
    'ciceksepeti': False,
    'temu': False,
}
```

---

## 🧩 Yeni Bir Site Ekleme

Projeyi genişletmek oldukça basit!

1. **Yeni Modül Oluşturun**  
   Örnek: `yenisite.py` dosyası oluşturun ve içinde `scrape()` fonksiyonunu tanımlayın.

2. **main.py'da Tanıtın**

   - İçe aktar:  
     ```python
     import yenisite
     ```

   - `SITES_TO_SCRAPE` sözlüğüne ekle:  
     ```python
     'yenisite': True
     ```

   - `SITE_MODULES` sözlüğüne ekle:  
     ```python
     'yenisite': yenisite
     ```

   - `SITE_ENGINES` sözlüğüne motor türünü belirt:  
     ```python
     'yenisite': 'selenium'
     ```

Artık yeni siteniz aktif bir şekilde tarama yapabilir!

---

## 📌 İpuçları

- **Tarama çok uzun sürüyorsa**, bazı siteleri devre dışı bırakabilirsiniz.
- **Captcha çözülemiyorsa**, manuel mod devreye girer — hızlıca çözmeniz gerekir.
- **Excel raporları** hem fiyatları hem de ürün bağlantılarını içerir.

---
