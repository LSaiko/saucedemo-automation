from selenium.webdriver.common.by import By
from .base_page import BasePage


class CartPage(BasePage):
    TITLE = (By.CLASS_NAME, "title")
    ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING = (By.ID, "continue-shopping")

    def item_names(self):
        self.find(self.CHECKOUT_BUTTON)  # cart-only element; URL flips before React renders the list
        return [e.text for e in self.driver.find_elements(*self.ITEM_NAMES)]

    def remove(self, name):
        self.click((By.ID, f"remove-{name.lower().replace(' ', '-')}"))

    def checkout(self):
        self.click(self.CHECKOUT_BUTTON)

    def continue_shopping(self):
        self.click(self.CONTINUE_SHOPPING)
