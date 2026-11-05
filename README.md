# saucedemo-automation

Selenium + pytest UI suite for [saucedemo.com](https://www.saucedemo.com): Page Objects, headless Chrome, pytest-html with screenshot-on-failure, pixel-diff visual regression. **37 tests: 32 pass, 5 xfail (known site bugs)**; cases in [docs/test-cases.md](docs/test-cases.md), latest results in [docs/test-results.md](docs/test-results.md).

## How this was built

1. Manually walked the login, inventory, cart and checkout flows and wrote every case down first -> [docs/test-cases.md](docs/test-cases.md)
2. Scaffolded the repo layout -> [scaffold.txt](scaffold.txt)
3. Built Page Object classes (`pages/`)
4. Wrote the per-test browser fixture (`conftest.py`)
5. Wrote tests against the POM classes only; no raw Selenium in `tests/`
6. Added pytest-html reporting with screenshot-on-failure
7. Wrote this README
8. Pushed to GitHub and pinned the repo
9. Parallel runs via pytest-xdist; CI matrix Python 3.11-3.15 on Linux + Windows/macOS on 3.14
10. Visual regression: `visual/visual_utils.py` (capture + Pillow compare, checked in isolation first), one login-page test confirmed stable on a second run, then inventory + cart, then the `--update-baselines` flag
11. Reviewed and committed the three baselines; first cross-OS CI run showed the font-rendering mismatch, fixed later with per-OS baseline dirs (see below)
12. Flaky-test retries via pytest-rerunfailures, with a `no_rerun` opt-out for validation tests (see below)

## Flaky Test Handling

- A failing test is retried up to 2 times, 3s apart (`--reruns 2 --reruns-delay 3` in `pytest.ini`) before it counts as a failure
- A test that passes only on a retry is reported as **flaky**, not passed: `FLAKY` / `f` in the terminal, a Flaky column in `reports/report.html`, and each failed attempt kept as a Rerun row with its screenshot
- Tests marked `@pytest.mark.no_rerun` (the login and checkout validation-error assertions) are never retried: a first-try failure there is a real bug
- `pytest --reruns 0` turns retries off for a debugging run
- What counts as flaky vs broken, why 2 reruns, and the exclusion list: [docs/flaky-policy.md](docs/flaky-policy.md)

## Visual regression

How it works:

1. Selenium (the `driver` fixture + Page Objects) drives the page to a state
2. `capture_screenshot` takes a full-page PNG via Chrome DevTools `Page.captureScreenshot` with `captureBeyondViewport`
3. `compare_screenshots` does a Pillow pixel diff against the baseline
4. Baselines live in `visual/baselines/<sys.platform>/` — `win32/`, `linux/`, `darwin/` — committed, one set per OS; each run writes the current shot plus a `<name>_diff.png` mask (white = changed pixels) to `visual/diffs/` (gitignored)
5. Tests (`tests/visual/`): login page, inventory page, cart with two items, plus `visual_user`'s inventory compared against the `standard_user` baseline (`xfail(strict=True)` — the persona's layout is deliberately broken and the diff catches it at ~3% changed)

Threshold:

- Fails if more than 2% of pixels changed (`threshold=0.02`)
- A pixel counts as changed only if any RGB channel differs by more than 32/255 (`PIXEL_TOLERANCE`)
- Why: sub-pixel anti-aliasing and font hinting shift edge pixels by small amounts across Chrome versions and OSes. The 32-level tolerance ignores those; 2% absorbs a few hundred edge pixels on a 1280-wide page but still fails on a moved button, a missing product card or a colour change (each well above 2%)
- A size mismatch fails outright

Running:

1. `pytest tests/visual` (xdist is on by default via `pytest.ini`; `-n0` runs serially)
2. No baseline yet: locally, the first run writes it and the test is SKIPPED with a message. Review the PNG, then commit it. In CI a missing baseline FAILS, so an OS can't silently lose coverage
3. Intentional UI change, your own OS: `pytest tests/visual --update-baselines`, eyeball the new PNGs, commit them
4. Intentional UI change, all OSes: Actions → CI → Run workflow → tick **update_baselines** (or `gh workflow run ci.yml -f update_baselines=true`). Every runner regenerates and uploads a `baselines-<os>-py<ver>` artifact; download, review, copy each OS's dir into `visual/baselines/`, commit
5. The flag overwrites the baselines; it does not blindly accept diffs. The PNG diff in the PR is the review artifact

Why per-OS baselines:

- Font rendering differs by OS (Windows DirectWrite, Linux FreeType, macOS CoreText): glyph shapes, hinting and subpixel positioning all differ, so a baseline from one OS won't match another pixel-for-pixel. Text-heavy pages can exceed 2% from fonts alone
- So each OS compares only against baselines captured on that OS. `win32/` came from Windows 11 locally; `linux/` and `darwin/` were captured on the GitHub runners themselves (Ubuntu 26.04, macOS), all Chrome headless at 1280x900
- Python version doesn't affect rendering: the five Linux jobs (3.11–3.15) produce byte-identical captures apart from a few hundred sub-tolerance anti-aliasing pixels, and all share `linux/`
- A runner-image or Chrome major bump can shift rendering enough to fail; that's what the weekly scheduled run catches. Regenerate with the `update_baselines` dispatch
- The saucedemo footer shows the current year, so baselines drift by a handful of pixels every January. Well under the threshold; regenerate if it ever tips over
