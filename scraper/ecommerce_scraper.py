from .product_list_page import ProductListPage
from uploader.woocommerce_uploader import WoocommerceUploader
from selenium import webdriver
import csv
import json

class EcommerceScraper:
    def __init__(self, start_url):
        self.start_url = start_url
        self.driver = webdriver.Chrome()
        self.products_data = []

    def scrape(self):
        self.driver.get(self.start_url)
        product_list_page = ProductListPage(self.driver)
        self.products_data = product_list_page.extract_products()

        # Upload to WooCommerce
        uploader = WoocommerceUploader()
        uploader.upload(self.products_data)

    def save_to_csv(self):
        filepath = "data/csv/output.csv"
        with open(filepath, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Price", "Category", "Details"]) # Modify headers as needed
            for product in self.products_data:
                writer.writerow([product['name'], product['price'], product['category'], product['details']])

    def save_to_json(self):
        filepath = "data/json/output.json"
        with open(filepath, 'w') as file:
            json.dump(self.products_data, file)

    def close(self):
        self.driver.close()
