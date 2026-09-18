# What's left

## Done
- [x] Manual walkthrough + test cases (`docs/test-cases.md`)
- [x] Page Objects, driver fixture, tests (33: 29 pass, 4 xfail)
- [x] pytest-html with screenshot-on-failure/xfail
- [x] README, results (`docs/test-results.md`)
- [x] Pushed to GitHub, CI green on every push
- [x] Chrome installed locally
- [x] Parallel runs via pytest-xdist (`-n auto`): ~60s local, ~56s CI
- [x] GitHub Actions bumped to v7 (no Node 20 warnings)
- [x] CI matrix: Python 3.10–3.14 on Linux + Windows/macOS on 3.14
- [x] Visual regression: Pillow pixel diff, 3 baselines (login/inventory/cart), `--update-baselines` flag; runs on Windows job only (36: 32 pass, 4 xfail)
- [x] Flakes fixed: visual capture waits for web fonts (`document.fonts`), `cart_count()` retries on stale badge; `visual/diffs/` uploaded as CI artifact on Windows failure. 3 green 7-job runs since

## Manual
- [ ] Pin the repo on your GitHub profile (no API for this): github.com/LSaiko → "Customize your pins" → `saucedemo-automation`

## Optional / when needed
- [ ] `visual_user` layout checks — reuse the `check_visual` fixture with a `visual_user` login and compare against the `standard_user` baselines
- [ ] Move credentials to `.env` (gitignored) if real accounts are ever used; saucedemo's public ones are fine hardcoded
- [ ] Per-OS baseline dirs (`visual/baselines/<platform>/`) so Linux/macOS CI jobs run the visual tests too (currently `skipif` win32 only)
