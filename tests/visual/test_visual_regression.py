import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from visual.visual_utils import BASELINES, capture_screenshot, compare_screenshots


@pytest.fixture
def check_visual(driver):
    def _check(name):
        current = capture_screenshot(driver, name)
        baseline = BASELINES / f"{name}.png"
        if current == baseline:
            pytest.skip(f"no baseline existed; wrote {baseline} - review and commit it")
        assert compare_screenshots(baseline, current), f"{name} differs from baseline; see {current.parent}"
    return _check


def _login(driver):
    LoginPage(driver).open().login("standard_user", "secret_sauce")
    inventory = InventoryPage(driver)
    inventory.item_names()  # wait for the product grid before shooting
    return inventory


def test_login_page(driver, check_visual):
    LoginPage(driver).open()
    check_visual("login_page")


def test_inventory_page(driver, check_visual):
    _login(driver)
    check_visual("inventory_page")


def test_cart_page_with_items(driver, check_visual):
    inventory = _login(driver)
    inventory.add_to_cart("Sauce Labs Backpack")
    inventory.add_to_cart("Sauce Labs Bike Light")
    inventory.go_to_cart()
    CartPage(driver).item_names()
    check_visual("cart_page")
