# Manual tasks to continue

- [X] Install Google Chrome locally (optional): Selenium Manager currently downloads Chrome for Testing on first run; a local install is faster and lets `webdriver-manager` take over.
- [ ] Move test credentials out of the tests if real accounts are ever used — add `.env` (gitignored) and load with `os.environ`; saucedemo's public `standard_user/secret_sauce` are fine hardcoded.
- [ ] Add CI (GitHub Actions) running `pytest` on push; Chrome for Testing works headless on `ubuntu-latest` with no extra setup.
- [ ] Cover remaining saucedemo users (`problem_user`, `performance_glitch_user`, `error_user`, `visual_user`) if their quirks matter to you.
- [ ] Automate the pending cases in `docs/test-cases.md` (L5-L6, I5-I6, C4, K3-K6).
