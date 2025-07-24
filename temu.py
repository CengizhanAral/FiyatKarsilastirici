import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

SITE_NAME = "Temu"
URL_TEMPLATE = 'https://www.temu.com/search_result.html?search_key={}'

LOCATORS = {
    'product_card': (By.CSS_SELECTOR, "div[data-tooltip^='goodContainer-']"),
    'link_and_title_container': (By.CSS_SELECTOR, "div[data-tooltip^='goodName-'] a"),
    'price_container': (By.CSS_SELECTOR, "div[data-type='price']"),
    'cookie_accept_button': (By.XPATH, "//button/div/span[text()='Accept all']"),
    'captcha_container': (By.ID, "Slider"),
    'slider_handle': (By.CSS_SELECTOR, "div.slide-btn-MhclW"),
    'slider_track': (By.CSS_SELECTOR, "div.slider-wrapper-2tige"),
    'captcha_refresh_button': (By.CSS_SELECTOR, "div.refresh-27d6x"),
}


def solve_slide_captcha(driver):
    """
    Temu'nun sürükle-bırak CAPTCHA'sını çözmeye çalışır.
    Çoğu zaman manuel olarak çözülmesi gerekir.
    """
    try:
        wait = WebDriverWait(driver, 5)
        captcha_container = wait.until(EC.visibility_of_element_located(LOCATORS['captcha_container']))
        slider_handle = wait.until(EC.element_to_be_clickable(LOCATORS['slider_handle']))
        slider_track = wait.until(EC.visibility_of_element_located(LOCATORS['slider_track']))

        print("  - Captcha algılandı, çözülmeye çalışılıyor...")

        track_width = slider_track.size['width']
        move_percentage = random.uniform(0.4, 0.55)
        move_distance = track_width * move_percentage
        actions = ActionChains(driver)
        actions.click_and_hold(slider_handle).perform()

        current_pos = 0
        while current_pos < move_distance:
            step = random.randint(15, 40)
            if current_pos + step > move_distance:
                step = move_distance - current_pos
            actions.move_by_offset(step, random.randint(-3, 3))
            actions.perform()
            current_pos += step
            time.sleep(random.uniform(0.05, 0.2))

        actions.release().perform()
        print("  - Captcha çözme denemesi tamamlandı. Sonuç kontrol ediliyor...")

        time.sleep(3)
        if not driver.find_elements(*LOCATORS['captcha_container']):
            print("  - Captcha başarıyla geçilmiş görünüyor!")
            return True
        else:
            print("  - Captcha denemesi başarısız.")
            return False

    except TimeoutException:
        print("  - Captcha bulunamadı, işleme devam ediliyor.")
        return True
    except Exception as e:
        print(f"  - Captcha çözülürken bir hata oluştu: {e}")
        return False


def scrape(driver, search_term, limit=5):
    """
    Popup bulursa kapatır. CAPTCHA arar, çözüme gönderir.
    Çözülemezse 10 saniyeye kadar manuel çözümü bekler.
    """
    results = []
    formatted_search_term = search_term.replace(' ', '+')
    url = URL_TEMPLATE.format(formatted_search_term)
    print(f"\n---> {SITE_NAME} taranıyor (Motor: Selenium)...")

    try:
        driver.get(url)

        try:
            cookie_wait = WebDriverWait(driver, 5)
            accept_button = cookie_wait.until(EC.element_to_be_clickable(LOCATORS['cookie_accept_button']))
            print("  - Çerez (cookie) pop-up'ı bulundu, kapatılıyor...")
            accept_button.click()
            time.sleep(1)
        except TimeoutException:
            print("  - Çerez pop-up'ı bulunamadı, bu adım atlanıyor.")

        max_attempts = 3
        captcha_solved = False
        for attempt in range(max_attempts):
            print(f"  - Captcha kontrolü yapılıyor (Otomatik Deneme {attempt + 1}/{max_attempts})...")
            if solve_slide_captcha(driver):
                captcha_solved = True
                break

            if attempt < max_attempts - 1:
                try:
                    print("  - Yeni bir captcha için yenileme butonuna basılıyor...")
                    refresh_button = driver.find_element(*LOCATORS['captcha_refresh_button'])
                    refresh_button.click()
                    time.sleep(2)
                except Exception:
                    print(f"  - Yenileme butonu bulunamadı veya tıklanamadı.")
                    time.sleep(2)

        # --- YENİ MANTIK: Manuel Çözüm için Bekleme ---
        if not captcha_solved:
            print("\n" + "=" * 50)
            print("  UYARI: Otomatik denemeler başarısız oldu.")
            print("  Lütfen captcha'yı 10 saniye içinde manuel olarak çözün.")
            print("=" * 50 + "\n")
            try:
                manual_wait = WebDriverWait(driver, 10)
                manual_wait.until(EC.invisibility_of_element_located(LOCATORS['captcha_container']))
                print("  - Captcha manuel olarak çözüldü. Devam ediliyor...")
            except TimeoutException:
                print(f"[{SITE_NAME}] Captcha 10 saniye içinde manuel olarak çözülmedi. Tarama durduruluyor.")
                return []

        wait = WebDriverWait(driver, 20)
        print("İlk ürün kartının belirmesi bekleniyor...")
        driver.execute_script("window.scrollTo(0, 1200);")
        time.sleep(3)

        wait.until(EC.presence_of_element_located(LOCATORS['product_card']))
        print("İlk ürün kartı yüklendi.")

        product_cards = driver.find_elements(*LOCATORS['product_card'])
        print(f"{len(product_cards)} adet ürün kartı bulundu ve ilk {limit} tanesi incelenecek...")

        count = 0
        for card in product_cards:
            if count >= limit:
                break

            try:
                link_element = card.find_element(*LOCATORS['link_and_title_container'])
                price_element = card.find_element(*LOCATORS['price_container'])
                title = link_element.text.strip()
                relative_link = link_element.get_attribute('href')
                link = 'https://www.temu.com' + relative_link if relative_link and relative_link.startswith(
                    '/') else relative_link
                price = price_element.text.replace('\n', '').strip() + " TL"

                if title and link:
                    results.append({'Site': SITE_NAME, 'Ürün Adı': title, 'Fiyat': price, 'URL': link})
                    print(f"  - {title[:60]}... -> {price}")
                    count += 1
            except NoSuchElementException:
                print("  - Standart dışı bir ürün kartı atlanıyor.")
                continue

    except TimeoutException:
        print(
            f"[{SITE_NAME}] Belirtilen sürede hiçbir ürün kartı yüklenemedi. Sayfa boş veya bot koruması aktif olabilir.")
    except Exception as e:
        print(f"[{SITE_NAME}] taranırken beklenmedik bir hata oluştu: {e}")

    if count == 0:
        print(f"  - {SITE_NAME} için geçerli ürün bulunamadı.")

    return results
