# kstore-scraper

## File/Folder Structure

    ecommerce_scraper/
    |-- main.py                     # Contains main execution logic.  Initialize 'EcommerceScraper' here
    |-- scraper/
    |   |-- __init__.py
    |   |-- ecommerce_scraper.py    # EcommerceScraper class initializes scraping process
    |   |-- product_list_page.py    # ProductListPage class
    |   |-- product_detail_page.py  # ProductDetailPage class
    |-- uploader/
    |   |-- __1init__.py
    |   |-- woocommerce_uploader.py # WoocommerceUploader class
    |-- utils/
    |   |-- __init__.py
    |   |-- helpers.py              # Any helper functions can be placed here.
    |-- config.py                   # To store configurations, e.g., start URLs, API keys, etc.

### Importing Modules

In **main.py**

```python
from scraper.ecommerce_scraper import EcommerceScraper
from config import START_URL

if __name__ == "__main__":
    scraper = EcommerceScraper(START_URL)
    scraper.scrape()

```

In **ecommerce_scraper.py**

```python
from .product_list_page import ProductListPage
from .product_detail_page import ProductDetailPage
from uploader.woocommerce_uploader import WoocommerceUploader

```

### Handling Data

#### CSV

```python
import csv

filepath = "data/csv/output.csv"
with open(filepath, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Header1", "Header2", ...])
    # ... Write the rows of data

```

```python
import json

filepath = "data/json/output.json"
with open(filepath, 'w') as file:
    json.dump(data_dict, file)

```

## Architecture

Given the complexity of the web scraping task at hand, it's essential to approach the problem in a modular and organized manner. Here's a high-level approach to the problem using an Object-Oriented Programming (OOP) methodology with Python:

### 1. Software Architecture:

**1.1 Classes and Responsibilities**:

- **EcommerceScraper**: Main class to initiate the scraping, it will utilize other classes to manage the overall flow.
- **ProductListPage**: Represents the initial product list page. Responsibilities include iterating over products and directing to the respective product detail page.
- **ProductDetailPage**: Handles the product detail page. Determines the type of mall area and delegates the scraping task to the respective handler.
- **WoocommerceUploader**: Responsible for uploading product data to the WooCommerce site.

**1.2 External Libraries**:

- Use `requests` or `selenium` for web scraping.
- Use `BeautifulSoup` for parsing the HTML content.

### 2. Modularized Steps:

**2.1 Initialization**:

- Instantiate `EcommerceScraper`.
- Setup a browser driver if using `selenium`.

**2.2 Product List Page**:

- Fetch the initial page with a list of products.
- Identify products using identifiable attributes/tags like class, ID, etc.
- For each product:
  - Extract name, price, categories, and mall area.
  - Depending on the mall area (쇼핑몰별 최저가 or 브랜드 카탈로그 or 브랜드스토어), instantiate respective detail page handler.

**2.3 Product Detail Page**:

- **If "쇼핑몰최저가"**:
  - Fetch the "판매처" table.
  - Iterate over links until one from brand.naver.com or smartstore.naver.com is found.
  - If found, collect "상세정보". Else, record the first URL and price.
- **If "브랜드 카탈로그"**:
  - Click on the brand link.
  - Scrape "상세정보" from the new page.
- **If "브랜드스토어"**:
  - Click on the name link.
  - Scrape "상세정보" from the new tab.

**2.4 Woocommerce Upload**:

- Use the `WoocommerceUploader` class to push the scraped data to WooCommerce. Consider using the WooCommerce API and python libraries like `woocommerce` for this.

**2.5 Error Handling & Logging**:

- Implement robust error handling to deal with unexpected webpage structures or missing data.
- Log essential steps and errors for debugging and tracking.

### 3. Other Considerations:

- **Rate Limiting**: Make sure to not overload the ecommerce site with requests. Introduce delays between requests using `time.sleep()`.
- **User Agent**: Use a legitimate user agent string to simulate a real browser and reduce the chances of being blocked.
- **Captcha**: Some ecommerce sites might introduce CAPTCHA challenges. Consider integrating CAPTCHA solving services if needed.
- **Data Storage**: Consider temporarily storing data in a local database or a structured file (like JSON) so that data is not lost in case of interruptions.
- **Concurrent Scraping**: Consider using `asyncio` with `aiohttp` or multi-threading to speed up the scraping process if the ecommerce site allows concurrent connections.

Finally, always respect `robots.txt` and terms of service of the ecommerce site. Web scraping might be against the site's terms of use, and scraping without permission can lead to legal repercussions.
