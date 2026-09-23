import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def pytest_addoption(parser):
    parser.addoption("--update-baselines", action="store_true",
                     help="overwrite visual/baselines/*.png with fresh screenshots instead of comparing")


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
    # execution_count comes from pytest-rerunfailures; >1 means earlier attempts failed
    if report.when == "call" and report.passed and getattr(item, "execution_count", 1) > 1:
        report.flaky = f"FLAKY: passed on attempt {item.execution_count}"  # plain attr, survives xdist


def pytest_collection_modifyitems(items):
    """no_rerun -> flaky(reruns=0); the per-test marker overrides the --reruns default from pytest.ini."""
    for item in items:
        if item.get_closest_marker("no_rerun"):
            item.add_marker(pytest.mark.flaky(reruns=0))


def pytest_report_teststatus(report):
    """Count passed-after-retry as 'flaky' in the terminal summary instead of 'passed'."""
    if getattr(report, "flaky", None):
        return "flaky", "f", "FLAKY"


def pytest_html_results_table_header(cells):
    cells.insert(2, "<th>Flaky</th>")


_rerun_rows_seen = set()


def pytest_html_results_table_row(report, cells):
    # pytest-html 4.2 re-emits every stored Rerun row after each attempt (rerunfailures logs a passed teardown
    # per attempt, which pytest-html reads as "test finished"); keep the first emission only
    if report.outcome == "rerun":
        if id(report) in _rerun_rows_seen:
            cells.clear()  # empty cells = pytest-html skips the row and its count
            return
        _rerun_rows_seen.add(id(report))
    cells.insert(2, f"<td>{getattr(report, 'flaky', '')}</td>")


pytest_html = pytest.importorskip("pytest_html")
