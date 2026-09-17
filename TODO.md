# Manual tasks to continue

- [ ] Install Google Chrome locally (optional): Selenium Manager currently downloads Chrome for Testing on first run; a local install is faster and lets `webdriver-manager` take over.
- [ ] Create a GitHub (or other) remote and push: `git remote add origin <url> && git push -u origin main`.
- [ ] Move test credentials out of the tests if real accounts are ever used — add `.env` (gitignored) and load with `os.environ`; saucedemo's public `standard_user/secret_sauce` are fine hardcoded.
- [ ] Add CI (GitHub Actions) running `pytest` on push; Chrome for Testing works headless on `ubuntu-latest` with no extra setup.
- [ ] Decide on screenshot-on-failure: hook `pytest_runtest_makereport` in `conftest.py` to attach `driver.get_screenshot_as_png()` to the pytest-html report.
- [ ] Cover remaining saucedemo users (`problem_user`, `performance_glitch_user`, `error_user`, `visual_user`) if their quirks matter to you.
