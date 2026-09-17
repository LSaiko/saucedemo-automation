
## How this was built

1. Manually walked the login, inventory, cart and checkout flows and wrote every case down first -> [docs/test-cases.md](docs/test-cases.md)
2. Scaffolded the repo layout -> [scaffold.txt](scaffold.txt)
3. Built Page Object classes (`pages/`)
4. Wrote the per-test browser fixture (`conftest.py`)
5. Wrote tests against the POM classes only; no raw Selenium in `tests/`
6. Added pytest-html reporting with screenshot-on-failure
7. Wrote this README
8. Pushed to GitHub and pinned the repo
