import pytest
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

ITEMS = ["Sauce Labs Backpack", "Sauce Labs Bike Light"]


@pytest.fixture
def checkout(driver):
    """Logged in, two items in cart, on the checkout info page. Yields (page, expected_subtotal)."""
    LoginPage(driver).open().login("standard_user", "secret_sauce")
    inventory = InventoryPage(driver)
    names, prices = inventory.item_names(), inventory.item_prices()
    expected = round(sum(prices[names.index(n)] for n in ITEMS), 2)
    for name in ITEMS:
        inventory.add_to_cart(name)
    inventory.go_to_cart()
    CartPage(driver).checkout()
    return CheckoutPage(driver), expected


def test_full_checkout_flow(checkout):
    page, expected_subtotal = checkout
    page.fill_info("John", "Doe", "12345")
    assert page.subtotal() == expected_subtotal
    assert page.total() == round(page.subtotal() + page.tax(), 2)
    page.finish()
    assert page.complete_message() == "Thank you for your order!"


def test_missing_first_name_shows_error(checkout):
    page, _ = checkout
    page.fill_info("", "Doe", "12345")
    assert "First Name is required" in page.error_message()


@pytest.mark.parametrize("first,last,zip_,msg", [
    ("John", "", "12345", "Last Name is required"),
    ("John", "Doe", "", "Postal Code is required"),
])
def test_missing_field_shows_error(checkout, first, last, zip_, msg):
    page, _ = checkout
    page.fill_info(first, last, zip_)
    assert msg in page.error_message()


def test_cancel_on_step_one_returns_to_cart(checkout):
    page, _ = checkout
    page.cancel()
    assert page.wait.until(EC.url_contains("/cart.html"))
    assert CartPage(page.driver).item_names() == ITEMS


def test_cancel_on_overview_returns_to_inventory(checkout):
    page, _ = checkout
    page.fill_info("John", "Doe", "12345")
    page.cancel()
    assert page.wait.until(EC.url_contains("/inventory.html"))


def test_back_home_clears_cart(checkout):
    page, _ = checkout
    page.fill_info("John", "Doe", "12345")
    page.finish()
    page.back_home()
    assert page.wait.until(EC.url_contains("/inventory.html"))
    assert InventoryPage(page.driver).cart_count() == 0
