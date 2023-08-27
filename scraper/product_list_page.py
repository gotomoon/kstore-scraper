from .product_detail_page import ProductDetailPage

class ProductListPage:
    def __init__(self, driver):
        self.driver = driver

    def extract_products(self):
        products = self.driver.find_elements_by_some_selector()  # Placeholder
        products_data = []

        for product in products:
            detail_page = ProductDetailPage(self.driver, product)
            product_data = detail_page.extract_detail()
            products_data.append(product_data)

        return products_data
