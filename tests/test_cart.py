import pytest
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"


@pytest.fixture
def cart(driver):
    LoginPage(driver).open().login("standard_user", "secret_sauce")
    inventory = InventoryPage(driver)
    inventory.add_to_cart(BACKPACK)
    inventory.add_to_cart(BIKE_LIGHT)
    inventory.go_to_cart()
    return CartPage(driver)


def test_cart_shows_added_items(cart):
    assert cart.item_names() == [BACKPACK, BIKE_LIGHT]


def test_remove_item_in_cart(cart):
    cart.remove(BACKPACK)
    assert cart.item_names() == [BIKE_LIGHT]


def test_continue_shopping_preserves_cart(cart):
    cart.continue_shopping()
    assert cart.wait.until(EC.url_contains("/inventory.html"))
    assert InventoryPage(cart.driver).cart_count() == 2
