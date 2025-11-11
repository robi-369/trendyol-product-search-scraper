thonimport requests
from bs4 import BeautifulSoup
import json
import os

class TrendyolScraper:
    def __init__(self, country_code="tr", use_proxy=False, proxies=None):
        self.base_url = "https://www.trendyol.com"
        self.country_code = country_code
        self.use_proxy = use_proxy
        self.proxies = proxies if proxies else {}
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def fetch_product_data(self, url):
        response = requests.get(url, headers=self.headers, proxies=self.proxies)
        if response.status_code != 200:
            print(f"Failed to fetch {url} with status code {response.status_code}")
            return None
        return response.text

    def parse_product_data(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        product = {
            "url": soup.find("link", {"rel": "canonical"})["href"],
            "title": soup.find("h1", {"class": "pr-new-br"}).text.strip(),
            "brand": soup.find("a", {"class": "link-brand"}).text.strip(),
            "image_url": soup.find("img", {"class": "p-image"})["src"],
            "total_reviews": soup.find("span", {"class": "rating-stars"})["data-rating-count"],
            "rating_score": soup.find("span", {"class": "rating-stars"})["data-rating"],
            "old_price": soup.find("span", {"class": "prc-dsc"}).text.strip(),
            "social_proof": [s.text.strip() for s in soup.find_all("span", {"class": "add-to-cart-count"})],
            "discount_percentage": soup.find("span", {"class": "discount-tag"}).text.strip() if soup.find("span", {"class": "discount-tag"}) else None,
            "lastest_price": soup.find("span", {"class": "prc-org"}).text.strip(),
            "currency": "TRY",  # Assuming currency as TRY for Turkey
            "promotion_name": soup.find("div", {"class": "discount-info"}).text.strip() if soup.find("div", {"class": "discount-info"}) else None,
            "from_url": url,
            "from_country_code": self.country_code
        }
        return product

    def save_to_file(self, data, filename="sample_output.json"):
        if not os.path.exists("data"):
            os.makedirs("data")
        with open(f"data/{filename}", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
    def scrape(self, product_urls):
        scraped_data = []
        for url in product_urls:
            html = self.fetch_product_data(url)
            if html:
                product_data = self.parse_product_data(html)
                if product_data:
                    scraped_data.append(product_data)
        self.save_to_file(scraped_data)
        return scraped_data