import pytest
from pages.login_page import LoginPage


@pytest.fixture
def login_page(driver):
    return LoginPage(driver).open()


def test_valid_login(login_page):
    login_page.login("standard_user", "secret_sauce")
    assert login_page.is_logged_in()


def test_locked_out_user(login_page):
    login_page.login("locked_out_user", "secret_sauce")
    assert "locked out" in login_page.error_message()


def test_wrong_password(login_page):
    login_page.login("standard_user", "wrong_password")
    assert "do not match" in login_page.error_message()


def test_empty_fields(login_page):
    login_page.login("", "")
    assert "Username is required" in login_page.error_message()
