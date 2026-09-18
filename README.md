
## How this was built

1. Manually walked the login, inventory, cart and checkout flows and wrote every case down first -> [docs/test-cases.md](docs/test-cases.md)
2. Scaffolded the repo layout -> [scaffold.txt](scaffold.txt)
3. Built Page Object classes (`pages/`)
4. Wrote the per-test browser fixture (`conftest.py`)
5. Wrote tests against the POM classes only; no raw Selenium in `tests/`
6. Added pytest-html reporting with screenshot-on-failure
7. Wrote this README
8. Pushed to GitHub and pinned the repo

## Visual regression

How it works:

1. Selenium (the `driver` fixture + Page Objects) drives the page to a state
2. `capture_screenshot` takes a full-page PNG via Chrome DevTools `Page.captureScreenshot` with `captureBeyondViewport`
3. `compare_screenshots` does a Pillow pixel diff against the baseline
4. Baselines live in `visual/baselines/` (committed); each run writes the current shot plus a `<name>_diff.png` mask (white = changed pixels) to `visual/diffs/` (gitignored)
5. Tests (`tests/visual/`): login page, inventory page, cart with two items

Threshold:

- Fails if more than 2% of pixels changed (`threshold=0.02`)
- A pixel counts as changed only if any RGB channel differs by more than 32/255 (`PIXEL_TOLERANCE`)
- Why: sub-pixel anti-aliasing and font hinting shift edge pixels by small amounts across Chrome versions and OSes. The 32-level tolerance ignores those; 2% absorbs a few hundred edge pixels on a 1280-wide page but still fails on a moved button, a missing product card or a colour change (each well above 2%)
- A size mismatch fails outright

Running:

1. `pytest tests/visual` (xdist is on by default via `pytest.ini`; `-n0` runs serially)
2. No baseline yet: the first run writes it and the test is SKIPPED with a message. Review the PNG, then commit it
3. Intentional UI change: `pytest tests/visual --update-baselines`, eyeball the new PNGs in `visual/baselines/`, commit them
4. The flag overwrites the baselines; it does not blindly accept diffs. The PNG diff in the PR is the review artifact

Known limitation - fonts:

- Font rendering differs between local (Windows, DirectWrite) and CI (Ubuntu, FreeType): glyph shapes, hinting and subpixel positioning all differ, so baselines from one OS will not match another pixel-for-pixel. Text-heavy pages can exceed 2% from fonts alone
- Mitigations: generate baselines on the same OS/Chrome that runs the comparison (regenerate in CI, or keep per-OS baseline dirs), or pin the Chrome version
- Current baselines: Windows 11 / Chrome headless at 1280x900
- The saucedemo footer shows the current year, so baselines drift by a handful of pixels every January. Well under the threshold; regenerate if it ever tips over
