"""saucedemo's deliberately broken users. Known bugs are xfail(strict=True):
the report captures a screenshot of the broken state, and if saucedemo ever
fixes one the strict xfail flips to a failure so we notice."""
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

BACKPACK = "Sauce Labs Backpack"
PERSONAS = ["problem_user", "error_user", "visual_user"]


def login_as(driver, user):
    LoginPage(driver).open().login(user, "secret_sauce")
    return InventoryPage(driver)


@pytest.mark.parametrize("user", PERSONAS)
def test_persona_can_log_in(driver, user):
    login_as(driver, user)
    assert "/inventory.html" in driver.current_url


@pytest.mark.parametrize("user", PERSONAS)
def test_persona_can_add_to_cart(driver, user):
    inventory = login_as(driver, user)
    inventory.add_to_cart(BACKPACK)
    assert inventory.cart_count() == 1


@pytest.mark.xfail(strict=True, reason="problem_user: sort dropdown is a no-op")
def test_problem_user_sort(driver):
    inventory = login_as(driver, "problem_user")
    inventory.sort_by("za")
    assert inventory.item_names() == sorted(inventory.item_names(), reverse=True)


@pytest.mark.xfail(strict=True, reason="problem_user: last-name field drops keystrokes")
def test_problem_user_checkout_info(driver):
    inventory = login_as(driver, "problem_user")
    inventory.add_to_cart(BACKPACK)
    inventory.go_to_cart()
    CartPage(driver).checkout()
    page = CheckoutPage(driver)
    page.fill_info("John", "Doe", "12345")
    assert "/checkout-step-two.html" in driver.current_url


@pytest.mark.xfail(strict=True, reason="error_user: sort raises 'Sorting is broken!' alert")
def test_error_user_sort(driver):
    inventory = login_as(driver, "error_user")
    inventory.sort_by("za")
    assert inventory.item_names() == sorted(inventory.item_names(), reverse=True)


@pytest.mark.xfail(strict=True, reason="error_user: Finish button does nothing")
def test_error_user_finish(driver):
    inventory = login_as(driver, "error_user")
    inventory.add_to_cart(BACKPACK)
    inventory.go_to_cart()
    CartPage(driver).checkout()
    page = CheckoutPage(driver)
    page.fill_info("John", "Doe", "12345")
    page.finish()
    assert page.complete_message() == "Thank you for your order!"
