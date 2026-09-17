# Manual tasks to continue

- [X] Install Google Chrome locally (optional): Selenium Manager currently downloads Chrome for Testing on first run; a local install is faster and lets `webdriver-manager` take over.
- [ ] Move test credentials out of the tests if real accounts are ever used — add `.env` (gitignored) and load with `os.environ`; saucedemo's public `standard_user/secret_sauce` are fine hardcoded.
