import shutil
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1280,900")
    # saucedemo triggers Chrome's password-leak popup on login; disable it
    opts.add_experimental_option("prefs", {"credentials_enable_service": False, "profile.password_manager_leak_detection": False})
    # ponytail: Selenium Manager downloads Chrome for Testing if no Chrome is installed;
    # webdriver-manager only resolves the driver, so use it only when a local Chrome exists
    service = Service(ChromeDriverManager().install()) if shutil.which("chrome") else None
    drv = webdriver.Chrome(service=service, options=opts)
    yield drv
    drv.quit()
