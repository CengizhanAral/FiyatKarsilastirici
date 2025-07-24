import requests
from bs4 import BeautifulSoup
import urllib.parse

# Siteye özel ayarlar
SITE_NAME = "Amazon"
URL_TEMPLATE = 'https://www.amazon.com.tr/s?k={}'
# Locators'ı daha sağlam bir yapıya geçiriyoruz.
# Önce ürün kartını, sonra kartın içindeki elemanları bulacağız.
LOCATORS = {
    'product_card': "div[data-component-type='s-search-result']",
    'title': "h2.a-text-normal span",
    'price_whole': "span.a-price-whole",
    'price_fraction': "span.a-price-fraction",
    'link': "a.a-link-normal.s-underline-text.s-link-style",
}


def scrape(search_term, limit=5):
    """
    Amazon.com.tr sitesini 'requests' ile daha sağlam bir yöntemle tarar.
    Önce ürün kartlarını bulur, sonra her kartın içinden bilgileri çeker.
    """
    results = []
    encoded_search_term = urllib.parse.quote_plus(search_term)
    url = URL_TEMPLATE.format(encoded_search_term)

    print(f"\n---> {SITE_NAME} taranıyor (Motor: Requests)...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        product_cards = soup.select(LOCATORS['product_card'])
        print(f"{len(product_cards)} adet potansiyel ürün kartı bulundu. İlk {limit} tanesi işlenecek...")

        count = 0
        for card in product_cards:
            if count >= limit:
                break

            title_element = card.select_one(LOCATORS['title'])
            price_whole_element = card.select_one(LOCATORS['price_whole'])
            price_fraction_element = card.select_one(LOCATORS['price_fraction'])
            link_element = card.select_one(LOCATORS['link'])

            if title_element and price_whole_element and link_element:
                title = title_element.get_text(strip=True)

                price_whole = price_whole_element.get_text(strip=True).replace('.', '')
                price_fraction = price_fraction_element.get_text(strip=True) if price_fraction_element else "00"
                price = f"{price_whole},{price_fraction} TL"

                link = "https://www.amazon.com.tr" + link_element.get('href', '#')

                # Bazı linkler reklam/yönlendirme linki olabilir, bunları filtreleyelim
                if '/sspa/' in link:
                    continue

                results.append({'Site': SITE_NAME, 'Ürün Adı': title, 'Fiyat': price, 'URL': link})
                print(f"  - {title[:60]}... -> {price}")
                count += 1

    except requests.exceptions.RequestException as e:
        print(f"[{SITE_NAME}] siteye erişirken bir ağ hatası oluştu: {e}")
    except Exception as e:
        print(f"[{SITE_NAME}] taranırken bir hata oluştu: {e}")

    if count == 0:
        print(f"  - {SITE_NAME} için geçerli ürün bulunamadı. Sitenin yapısı değişmiş olabilir.")

    return results
