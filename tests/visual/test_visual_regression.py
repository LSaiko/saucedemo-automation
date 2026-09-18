import sys

import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from visual.visual_utils import BASELINES, capture_screenshot, compare_screenshots

# ponytail: baselines captured on Windows only; per-OS baseline dirs when Linux/mac visual coverage is needed (README)
pytestmark = pytest.mark.skipif(sys.platform != "win32", reason="visual baselines captured on Windows; see README")


@pytest.fixture
def check_visual(driver, request):
    def _check(name, baseline_name=None):
        baseline = BASELINES / f"{baseline_name or name}.png"
        if request.config.getoption("--update-baselines") and not baseline_name:
            baseline.unlink(missing_ok=True)  # capture_screenshot then writes a fresh baseline
        current = capture_screenshot(driver, name, baseline)
        if current == baseline:
            pytest.skip(f"no baseline existed; wrote {baseline} - review and commit it")
        assert compare_screenshots(baseline, current), f"{name} differs from baseline; see {current.parent}"
    return _check


def _login(driver, user="standard_user"):
    LoginPage(driver).open().login(user, "secret_sauce")
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


@pytest.mark.xfail(strict=True, reason="visual_user: inventory layout is deliberately broken (shifted cart icon/buttons, wrong product image)")
def test_visual_user_inventory_matches_standard(driver, check_visual):
    _login(driver, "visual_user")
    check_visual("visual_user_inventory", baseline_name="inventory_page")
