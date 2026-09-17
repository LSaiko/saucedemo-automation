import pytest
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
