import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Siteye özel ayarlar
SITE_NAME = "N11"
URL_TEMPLATE = 'https://www.n11.com/arama?q={}'
LOCATORS = {
    'product_card': (By.CSS_SELECTOR, "li.column"),
    'card_link': (By.CSS_SELECTOR, "a.plink"),
    'card_title_element': (By.CLASS_NAME, "productName"),
    'card_price': (By.CSS_SELECTOR, "div.priceContainer ins, div.priceContainer span.newPrice"), # İndirimli ve indirimsiz fiyatlar için
}


def scrape(driver, search_term, limit=5):
    """
    N11'i tarar ve ürün bilgilerini döndürür.
    """
    results = []
    url = URL_TEMPLATE.format(search_term)
    print(f"\n---> {SITE_NAME} taranıyor (Motor: Selenium)...")
    driver.get(url)
    wait = WebDriverWait(driver, 20)

    try:
        print("İlk ürün kartının yüklenmesi bekleniyor...")
        wait.until(EC.presence_of_element_located(LOCATORS['product_card']))
        print("İlk ürün kartı yüklendi.")
        driver.execute_script("window.scrollTo(0, 800);")
        time.sleep(2)

        product_cards = driver.find_elements(*LOCATORS['product_card'])[:limit]
        print(f"{len(product_cards)} adet ürün kartı bulundu ve incelenecek...")

        for card in product_cards:
            title, price, link = "Başlık Bulunamadı", "Fiyat Bulunamadı", "#"
            try:
                link_element = card.find_element(*LOCATORS['card_link'])
                link = link_element.get_attribute('href')
                title_element = card.find_element(*LOCATORS['card_title_element'])
                title = title_element.text.strip()
                price_element = card.find_element(*LOCATORS['card_price'])
                price = price_element.text.strip()

                if not title: title = "Başlık Bulunamadı"
                results.append({'Site': SITE_NAME, 'Ürün Adı': title, 'Fiyat': price, 'URL': link})
                print(f"  - {title[:60]}... -> {price}")
            except NoSuchElementException:
                print("  - Bir kartın iç yapısı standart dışı, atlanıyor.")
                continue
    except TimeoutException:
        print(f"[{SITE_NAME}] Belirtilen sürede hiçbir ürün kartı yüklenemedi.")
    except Exception as e:
        print(f"[{SITE_NAME}] taranırken bir hata oluştu: {e}")

    return results
