# What's left

## Done
- [x] Manual walkthrough + test cases (`docs/test-cases.md`)
- [x] Page Objects, driver fixture, tests (now 37: 32 pass, 5 xfail)
- [x] pytest-html with screenshot-on-failure/xfail
- [x] README, results (`docs/test-results.md`)
- [x] Pushed to GitHub, CI green on every push + weekly scheduled run
- [x] Chrome installed locally
- [x] Parallel runs via pytest-xdist (`-n auto`): ~60s local, ~56s CI
- [x] GitHub Actions bumped to v7 (no Node 20 warnings)
- [x] CI matrix: Python 3.11–3.15 on Linux + Windows/macOS on 3.14 (3.10 dropped, EOL)
- [x] Visual regression: Pillow pixel diff, 3 baselines (login/inventory/cart), `--update-baselines` flag; runs on Windows job only (36: 32 pass, 4 xfail)
- [x] Flakes fixed: visual capture waits for web fonts (`document.fonts`), `cart_count()` retries on stale badge; `visual/diffs/` uploaded as CI artifact on Windows failure. 3 green 7-job runs since
- [x] `visual_user` layout check: inventory vs the `standard_user` baseline, `xfail(strict=True)` (37: 32 pass, 5 xfail)
- [x] Repo topics + description set; tagged and released [v1.0.0](https://github.com/LSaiko/saucedemo-automation/releases/tag/v1.0.0)
- [x] Maintenance pass 2026-11-05 (suite still green after 6 weeks idle): weekly CI cron + `workflow_dispatch`, Dependabot (pip + actions), MIT LICENSE, dependency floors raised to installed majors, chromedriver resolved once per session instead of per test, stale branch pruned. Verified on Ubuntu 26.04 runners and Python 3.15

## Manual
- [ ] Pin the repo on your GitHub profile (no API for this): github.com/LSaiko → "Customize your pins" → `saucedemo-automation`

## Recurring
- [ ] Review/merge the weekly Dependabot PR (grouped: all pip deps in one PR, actions in another)
- [ ] Check the Monday scheduled CI run; a red run with no commit means saucedemo, Chrome, or the runner image changed

## Optional / when needed
- [ ] `requirements.lock` (pip-compile) if reproducible runs ever matter more than testing against today's stack
- [ ] Move credentials to `.env` (gitignored) if real accounts are ever used; saucedemo's public ones are fine hardcoded
- [ ] Per-OS baseline dirs (`visual/baselines/<platform>/`) so Linux/macOS CI jobs run the visual tests too (currently `skipif` win32 only)
