class ProductDetailPage:
    def __init__(self, driver, product):
        self.driver = driver
        self.product = product

    def extract_detail(self):
        # Your extraction logic based on the website structure
        return {
            "name": "Extracted name",
            "price": "Extracted price",
            "category": "Extracted category",
            "details": "Extracted details"
        }
