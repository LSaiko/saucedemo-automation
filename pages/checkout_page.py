from selenium.webdriver.common.by import By
from .base_page import BasePage


class CheckoutPage(BasePage):
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    FINISH_BUTTON = (By.ID, "finish")
    ERROR = (By.CSS_SELECTOR, "[data-test='error']")
    SUMMARY_ITEMS = (By.CLASS_NAME, "cart_item")
    SUBTOTAL = (By.CLASS_NAME, "summary_subtotal_label")
    TAX = (By.CLASS_NAME, "summary_tax_label")
    TOTAL = (By.CLASS_NAME, "summary_total_label")
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    def fill_info(self, first, last, postal):
        self.type(self.FIRST_NAME, first)
        self.type(self.LAST_NAME, last)
        self.type(self.POSTAL_CODE, postal)
        self.click(self.CONTINUE_BUTTON)

    def error_message(self):
        return self.text_of(self.ERROR)

    @staticmethod
    def _money(label):
        return float(label.split("$")[1])

    def subtotal(self):
        return self._money(self.text_of(self.SUBTOTAL))

    def tax(self):
        return self._money(self.text_of(self.TAX))

    def total(self):
        return self._money(self.text_of(self.TOTAL))

    def finish(self):
        self.click(self.FINISH_BUTTON)

    def complete_message(self):
        return self.text_of(self.COMPLETE_HEADER)
