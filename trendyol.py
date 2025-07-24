import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

SITE_NAME = "Trendyol"
URL_TEMPLATE = 'https://www.trendyol.com/sr?q={}'
LOCATORS = {
    'data_script': (By.XPATH, "//script[contains(text(), '__SEARCH_APP_INITIAL_STATE__')]"),
}


def scrape(driver, search_term, limit=5):
    """
    Trendyol'un sayfa içindeki JSON verisini tarar ve ürün bilgilerini döndürür.
    """
    results = []
    url = URL_TEMPLATE.format(search_term)
    print(f"\n---> {SITE_NAME} taranıyor (Motor: Selenium/JSON)...")
    driver.get(url)
    wait = WebDriverWait(driver, 20)

    try:
        print("Sayfa içindeki veri paketi (JSON) bekleniyor...")
        script_element = wait.until(EC.presence_of_element_located(LOCATORS['data_script']))
        script_content = script_element.get_attribute('innerHTML')
        json_data_str = script_content.split(' = ', 1)[1].split(';', 1)[0].strip()

        data = json.loads(json_data_str)
        products = data.get('products', [])
        print(f"{len(products)} adet ürün veri paketinde bulundu. İlk {limit} tanesi işleniyor...")

        for product in products[:limit]:
            product_name = product.get('name', 'Başlık Bulunamadı')
            product_brand = product.get('brand', {}).get('name', '')
            full_title = f"{product_brand} {product_name}".strip()

            price_info = product.get('price', {})
            price_value = price_info.get('sellingPrice', 0)
            price = f"{price_value:,.2f} TL".replace(',', 'X').replace('.', ',').replace('X',
                                                                                         '.')  # Türk Lirası formatı

            url_slug = product.get('url', '#')
            full_url = f"https://www.trendyol.com{url_slug}"

            results.append({'Site': SITE_NAME, 'Ürün Adı': full_title, 'Fiyat': price, 'URL': full_url})
            print(f"  - {full_title[:60]}... -> {price}")

    except TimeoutException:
        print(f"[{SITE_NAME}] Veri paketi (JSON script) belirtilen sürede bulunamadı.")
    except (IndexError, AttributeError):
        print(f"[{SITE_NAME}] Sayfa yapısı değişmiş. JSON verisi beklenen formatta alınamadı.")
    except json.JSONDecodeError as e:
        print(f"[{SITE_NAME}] JSON verisi işlenirken hata oluştu. Muhtemelen veri formatı bozuk. Hata: {e}")
    except Exception as e:
        print(f"[{SITE_NAME}] taranırken beklenmedik bir hata oluştu: {e}")

    return results
