import pytest
from pages.login_page import LoginPage
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


def test_login_page(driver, check_visual):
    LoginPage(driver).open()
    check_visual("login_page")
