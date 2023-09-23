# kstore-scraper

## File/Folder Structure

```

EcommerceScraperProject/ # Root directory for your scraper project
|
|-- main.py # Main execution logic. Initialize and call EcommerceScraper from here
|
|-- scraper/ # Directory containing all scraping related modules
| |-- **init**.py # Initialization file for the scraper package
| |
| |-- ecommerce_scraper.py # Contains the EcommerceScraper class; main scraping logic
| |
| |-- product_list_page.py # Contains the ProductListPage class; methods related to scraping product listings
| |
| |-- product_detail_page.py # Contains the ProductDetailPage class; methods for scraping product details
|
|-- uploader/ # Directory for all upload-related modules
| |-- **init**.py # Initialization file for the uploader package
| |
| |-- woocommerce_uploader.py # Contains the WoocommerceUploader class; logic to upload scraped details
|
|-- utils/ # Directory for utility functions and classes
| |-- **init**.py # Initialization file for the utils package
| |
| |-- helpers.py # Contains helper functions; utility operations, data formatting, exception handling
|
|-- config.py # Configuration file; contains global configurations, start URLs, API keys, etc.

```

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

## Product Category Page Workflow:

Upon accessing the product category pages, products can belong to one of three distinct "mall types":

1. 쇼핑몰최저가
2. 브랜드 카탈로그
3. 브랜드 스토어

Depending on the mall type, the scraping workflow varies:

---

**1. Mall Type: 쇼핑몰최저가**

- Upon clicking a product, three scenarios can arise:

  **Case 1:** The product details page displays "브랜드 공식판매처".

  - Action: Extract the lowest price listed on the page.
  - Next, click on the "브랜드 공식판매처" link.
  - Proceed to scrape the product details from the resulting page.

  **Case 2:** The product details page doesn't display "브랜드 공식판매처" but showcases a list of malls under "판매처".

  - Action: Start clicking on the listed malls, beginning from the top.
  - Continue until a new tab opens displaying either "smartstore.naver.com" or "search.shopping.naver/catalog" in the URL. This indicates the link may lead to a different page.
  - Once the desired URL is found, scrape the product details from that page. Any subsequent malls in the "판매처" list can be ignored.

  **Case 3:** If neither "smartstore.naver.com" nor "search.shopping.naver/catalog" appear:

  - Action: Click the "최저가 사러가기" button.
  - Save the resulting URL for further actions.

---

**2. Mall Type: 브랜드 카탈로그**

- Action: Click on "브랜드 카탈로그".
- Proceed to scrape the product details from the resulting page.

---

**3. Mall Type: 브랜드 스토어**

- Action: Click on "브랜드 스토어".
- Proceed to scrape the product details from the resulting page.

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

---
