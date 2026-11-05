# What's left

## Done
- [x] Manual walkthrough + test cases (`docs/test-cases.md`)
- [x] Page Objects, driver fixture, tests (now 37: 32 pass, 5 xfail)
- [x] pytest-html with screenshot-on-failure/xfail
- [x] README, results (`docs/test-results.md`)
- [x] Pushed to GitHub, CI green on every push + weekly scheduled run
- [x] Chrome installed locally; project `.venv` built from the lock (keep using it: the lock's Pillow 13 conflicts with gradio in the global Python)
- [x] Parallel runs via pytest-xdist (`-n auto`): ~60s local, ~56s CI
- [x] GitHub Actions bumped to v7 (no Node 20 warnings)
- [x] CI matrix: Python 3.11–3.15 on Linux + Windows/macOS on 3.14 (3.10 dropped, EOL)
- [x] Visual regression: Pillow pixel diff, 3 baselines (login/inventory/cart), `--update-baselines` flag; initially Windows-only, now all OSes (see per-OS baselines below)
- [x] Flakes fixed: visual capture waits for web fonts (`document.fonts`), `cart_count()` retries on stale badge; `visual/diffs/` uploaded as CI artifact on failure (now from every job). 3 green 7-job runs since
- [x] `visual_user` layout check: inventory vs the `standard_user` baseline, `xfail(strict=True)` (37: 32 pass, 5 xfail)
- [x] Repo topics + description set; tagged and released [v1.0.0](https://github.com/LSaiko/saucedemo-automation/releases/tag/v1.0.0)
- [x] Maintenance pass 2026-11-05 (suite still green after 6 weeks idle): weekly CI cron + `workflow_dispatch`, Dependabot (pip + actions), MIT LICENSE, dependency floors raised to installed majors, chromedriver resolved once per session instead of per test, stale branch pruned. Verified on Ubuntu 26.04 runners and Python 3.15
- [x] First grouped Dependabot PR ([#2](https://github.com/LSaiko/saucedemo-automation/pull/2)) merged: floors raised to current versions
- [x] Per-OS visual baselines (`visual/baselines/{win32,linux,darwin}/`): all 7 CI jobs run the visual tests; Linux/macOS baselines generated on the runners via the `update_baselines` dispatch input; missing baseline fails in CI. Merged via [#3](https://github.com/LSaiko/saucedemo-automation/pull/3); 37 run, 0 skipped on every job
- [x] `requirements.lock`: exact universal pins via `uv pip compile` (all OSes, Python 3.11+); CI installs it; a `lock` job fails when `requirements.txt` outgrows it (verified: ignores upstream releases, catches floor bumps). Merged via [#4](https://github.com/LSaiko/saucedemo-automation/pull/4); CI is now 8 jobs (`lock` + 7 test)
- [x] README Setup / Run / Coverage / CI sections + CI badge restored (lost to a failed write in `2581c80` on 2026-09-16) and updated for the venv + lock workflow

## Manual
- [ ] Pin the repo on your GitHub profile (no API for this): github.com/LSaiko → "Customize your pins" → `saucedemo-automation`

## Recurring
- [ ] Review/merge the weekly Dependabot PR (grouped: all pip deps in one PR, actions in another). If its `lock` job fails, check out the PR branch, run `uv pip compile requirements.txt --universal --python-version 3.11 -o requirements.lock`, commit, push
- [ ] Check the Monday scheduled CI run; a red run with no commit means saucedemo, Chrome, or the runner image changed (visual failure on one OS only → regenerate that OS's baselines via the `update_baselines` dispatch)

## Optional / when needed
- [ ] Refresh the lock to latest occasionally: same command plus `--upgrade` (Dependabot only moves the floors)
- [ ] Move credentials to `.env` (gitignored) if real accounts are ever used; saucedemo's public ones are fine hardcoded
