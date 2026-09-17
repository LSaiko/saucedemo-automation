# saucedemo-automation

Selenium WebDriver + pytest UI test suite for [saucedemo.com](https://www.saucedemo.com).

## What it demonstrates

- **Page Object Model** — one class per page in `pages/`, locators as class constants, actions as methods.
- **Explicit waits only** — every lookup goes through `WebDriverWait` + `expected_conditions` in `pages/base_page.py`; no `time.sleep()`.
- **Function-scoped `driver` fixture** (`conftest.py`) — fresh headless Chrome per test, quit afterwards.
- **HTML reporting** via `pytest-html`, configured in `pytest.ini`.

## Coverage

| File | Scenarios |
|---|---|
| `tests/test_login.py` | valid login, locked-out user, wrong password, empty fields |
| `tests/test_inventory.py` | add/remove from cart badge, sort A–Z / Z–A / price low–high / high–low |
| `tests/test_cart.py` | cart contents, remove item, continue shopping keeps cart |
| `tests/test_checkout.py` | full checkout with totals verification, missing-info validation |

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows  (source .venv/bin/activate on macOS/Linux)
pip install -r requirements.txt
```

Chrome: if installed, `webdriver-manager` resolves the matching chromedriver. If not, Selenium Manager downloads Chrome for Testing automatically on first run.

## Run

```bash
pytest
```

`pytest.ini` already adds `--html=reports/report.html --self-contained-html`, so every run writes a single-file report to `reports/report.html`. Open it in a browser.

Run one file or show output verbosely:

```bash
pytest tests/test_login.py -v
```

To watch the browser, remove `--headless=new` in `conftest.py`.
