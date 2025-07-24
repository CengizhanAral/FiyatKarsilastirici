import pandas as pd
from datetime import datetime
import undetected_chromedriver as uc
import amazon
import hepsiburada
import trendyol
import n11
import ciceksepeti
import temu

# --- AYARLAR ---
"""
Hangi sitelerin kontrol edileceği buradan yönetilir.
True: Kontrol edilsin, False: Devre dışı
Temu'da popup ve CAPTCHA'lar sebebiyle düzgün çalışmayabilir.
Eğer 3 denemede çözemezse, bir süre çözülmesini bekler.
"""
SITES_TO_SCRAPE = {
    'amazon': True,
    'hepsiburada': True,
    'trendyol': True,
    'n11': True,
    'ciceksepeti': True,
    'temu': True,
}

SITE_MODULES = {
    'amazon': amazon,
    'hepsiburada': hepsiburada,
    'trendyol': trendyol,
    'n11': n11,
    'ciceksepeti': ciceksepeti,
    'temu': temu,
}

SITE_ENGINES = {
    'amazon': 'requests',
    'hepsiburada': 'selenium',
    'trendyol': 'selenium',
    'n11': 'selenium',
    'ciceksepeti': 'selenium',
    'temu': 'selenium',
}

def main():
    search_term = input("Aranacak ürünün adını girin: ")
    while True:
        try:
            limit_str = input("Her siteden kaç ürün listelensin? (Varsayılan: 5): ")
            if not limit_str:
                limit = 5
                break
            limit = int(limit_str)
            break
        except ValueError:
            print("Lütfen geçerli bir sayı girin.")

    print(f"\n'{search_term}' için fiyat araştırması başlıyor (her siteden max {limit} ürün)...")

    selenium_needed = any(
        SITE_ENGINES[site] == 'selenium' for site, active in SITES_TO_SCRAPE.items() if active
    )
    driver = None
    if selenium_needed:
        print("Selenium motoru hazırlanıyor...")
        try:
            options = uc.ChromeOptions()
            driver = uc.Chrome(options=options, use_subprocess=True)
            print("Selenium motoru başarıyla başlatıldı.")
        except Exception as e:
            print(f"Uyarı: Selenium sürücüsü başlatılamadı. Chrome'un yüklü olduğundan emin olun. Hata: {e}")
            driver = None

    all_results = []
    for site_name, is_active in SITES_TO_SCRAPE.items():
        if not is_active:
            continue

        module = SITE_MODULES[site_name]
        engine = SITE_ENGINES[site_name]

        try:
            if engine == 'selenium':
                if driver:
                    site_results = module.scrape(driver, search_term, limit)
                    all_results.extend(site_results)
            elif engine == 'requests':
                site_results = module.scrape(search_term, limit)
                all_results.extend(site_results)
        except Exception as e:
            print(f"!!! {site_name.title()} taranırken beklenmedik bir ana hata oluştu: {e}")

    if driver:
        driver.quit()
        print("\nSelenium motoru kapatıldı.")

    if not all_results:
        print("\nHiçbir siteden sonuç alınamadı.")
        return

    df = pd.DataFrame(all_results)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_search_term = "".join(c for c in search_term if c.isalnum())
    filename = f"FiyatRaporu_{safe_search_term}_{timestamp}.xlsx"

    try:
        df.to_excel(filename, index=False)
        print(f"\n✅ İşlem tamamlandı! Rapor '{filename}' adıyla kaydedildi.")
    except Exception as e:
        print(f"\n❌ Rapor dosyası kaydedilirken bir hata oluştu: {e}")


if __name__ == "__main__":
    main()