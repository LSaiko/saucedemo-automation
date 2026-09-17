from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage


class InventoryPage(BasePage):
    TITLE = (By.CLASS_NAME, "title")
    ITEMS = (By.CLASS_NAME, "inventory_item")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    ADD_BUTTONS = (By.CSS_SELECTOR, "button[id^='add-to-cart']")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, "button[id^='remove']")
    SORT_SELECT = (By.CLASS_NAME, "product_sort_container")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")

    @staticmethod
    def _slug(name):
        return name.lower().replace(" ", "-")

    def add_to_cart(self, name):
        self.click((By.ID, f"add-to-cart-{self._slug(name)}"))

    def remove_from_cart(self, name):
        self.click((By.ID, f"remove-{self._slug(name)}"))

    def item_names(self):
        return [e.text for e in self.find_all(self.ITEM_NAMES)]

    def item_prices(self):
        return [float(e.text.lstrip("$")) for e in self.find_all(self.ITEM_PRICES)]

    def sort_by(self, value):
        """value: az | za | lohi | hilo"""
        Select(self.find(self.SORT_SELECT)).select_by_value(value)

    def cart_count(self):
        badges = self.driver.find_elements(*self.CART_BADGE)
        return int(badges[0].text) if badges else 0

    def go_to_cart(self):
        self.click(self.CART_LINK)
        self.wait.until(EC.url_contains("/cart.html"))
