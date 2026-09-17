import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver(request):
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1280,900")
    # saucedemo triggers Chrome's password-leak popup on login; disable it
    opts.add_experimental_option("prefs", {"credentials_enable_service": False, "profile.password_manager_leak_detection": False})
    drv = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    request.node._driver = drv  # for the screenshot hook below
    yield drv
    drv.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach a screenshot to the pytest-html report on failure (and on xfail, so known site bugs are captured)."""
    report = (yield).get_result()
    drv = getattr(item, "_driver", None)
    if report.when == "call" and (report.failed or hasattr(report, "wasxfail")) and drv:
        extras = getattr(report, "extras", [])
        try:
            extras.append(pytest_html.extras.image(drv.get_screenshot_as_base64()))
            extras.append(pytest_html.extras.url(drv.current_url))
        except WebDriverException as e:  # e.g. open alert or hung renderer; a report extra must never kill the run
            extras.append(pytest_html.extras.text(f"screenshot unavailable: {e.__class__.__name__}"))
        report.extras = extras


pytest_html = pytest.importorskip("pytest_html")
