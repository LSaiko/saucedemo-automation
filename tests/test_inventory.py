import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"


@pytest.fixture
def inventory(driver):
    LoginPage(driver).open().login("standard_user", "secret_sauce")
    return InventoryPage(driver)


def test_add_one_item(inventory):
    inventory.add_to_cart(BACKPACK)
    assert inventory.cart_count() == 1


def test_add_two_remove_one(inventory):
    inventory.add_to_cart(BACKPACK)
    inventory.add_to_cart(BIKE_LIGHT)
    inventory.remove_from_cart(BACKPACK)
    assert inventory.cart_count() == 1


def test_sort_by_name(inventory):
    names = inventory.item_names()
    inventory.sort_by("az")
    assert inventory.item_names() == sorted(names)
    inventory.sort_by("za")
    assert inventory.item_names() == sorted(names, reverse=True)


def test_sort_by_price(inventory):
    inventory.sort_by("lohi")
    prices = inventory.item_prices()
    assert prices == sorted(prices)
    inventory.sort_by("hilo")
    prices = inventory.item_prices()
    assert prices == sorted(prices, reverse=True)


def test_item_detail_and_back(inventory):
    assert inventory.open_item(BACKPACK) == BACKPACK
    inventory.back_to_products()
    assert len(inventory.item_names()) == 6


def test_logout(inventory):
    inventory.logout()
    assert inventory.driver.current_url == "https://www.saucedemo.com/"
