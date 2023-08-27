from scraper.ecommerce_scraper import EcommerceScraper
from config import START_URL

if __name__ == "__main__":
    scraper = EcommerceScraper(START_URL)
    scraper.scrape()
    scraper.save_to_csv()
    scraper.save_to_json()
    scraper.close()
