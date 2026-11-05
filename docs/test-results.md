# Functionality test plan — results

**Date:** 2026-11-05 · **CI:** [run 42056471764](https://github.com/LSaiko/saucedemo-automation/actions/runs/42056471764) (headless Chrome, 7-job matrix: Ubuntu 26.04 × Python 3.11–3.15, Windows + macOS × 3.14)

**37 tests: 32 passed, 5 xfailed (known site bugs), 0 failed, 0 skipped — on every one of the 7 jobs.** Visual tests now run on all three OSes against per-OS baselines. Wall time: Linux 42–57s (3.15: 111s), macOS 99s, Windows 117s.

Test cases are defined in [test-cases.md](test-cases.md).

| Area | Cases | Pass | Known bug (xfail) | Notes |
|---|---|---|---|---|
| Login | L1–L6 | 6 | – | valid, locked-out, wrong pw, empty user, empty pw, performance_glitch |
| Inventory | I1–I6 | 6 | – | add/remove badge, sort A–Z/Z–A/price ↑↓, item detail + back, logout |
| Cart | C1–C4 | 4 | – | contents, remove, continue shopping keeps cart, empty-cart checkout allowed |
| Checkout | K1–K6 | 7 | – | totals verified (subtotal = Σ prices, total = subtotal + tax), first/last/zip validation, cancel from step one/overview, back-home clears cart |
| Personas | P1–P6 | 6 | 4 | see defects below |
| Visual | V1–V4 | 3 | 1 | login, inventory, cart-with-items screenshots vs committed baselines; ≤2% pixel change, 32/255 per-channel tolerance. V4: visual_user inventory vs standard baseline |

## Site defects found

All are pre-existing, intentional saucedemo demo behaviour. Each is marked `xfail(strict=True)` with a screenshot of the broken state attached to `reports/report.html`; the test turns red if saucedemo ever fixes it.

1. `problem_user` — sort dropdown has no effect (P3)
2. `problem_user` — checkout last-name input discards keystrokes (P4)
3. `error_user` — sorting raises a "Sorting is broken!" alert (P5)
4. `error_user` — Finish does not complete the order (P6)
5. Any user — an empty cart can proceed to checkout step one (C4, asserted as current behaviour, not xfail)
6. `visual_user` — inventory layout broken: dog photo for the backpack, cart icon and product titles shifted, randomised prices, last Add-to-cart button offset (V4). Pixel diff vs the standard baseline: 2.98% changed, i.e. caught with ~1 point of margin over the 2% threshold

No fixes required on the suite side: the defects are in the application under test.

## Stability

Two transient `TimeoutException`s (cold Chrome start + slow first page load) seen during initial development; resolved by raising the base explicit wait from 10s to 15s. Zero flakes since across ~10 local and 3 CI runs.

Two more flakes surfaced once the CI matrix grew to 7 jobs per push:

1. `test_login_page` (visual) failed on Windows in 3 of 4 consecutive runs — the screenshot fired before saucedemo's web font finished loading, so fallback glyphs pushed the diff past 2%. Fixed by also waiting for `document.fonts.status === 'loaded'` before capture (`8ae31b3`); 0 of 5 runs since.
2. `test_continue_shopping_preserves_cart` hit `StaleElementReferenceException` once on Ubuntu — `InventoryPage.cart_count()` read `.text` on a badge React had re-rendered. Fixed by running find + read inside `retry_wait` (`9e8fe04`).

`visual/diffs/` is uploaded as a CI artifact when any job fails, so future visual flakes can be inspected rather than guessed at.

## Visual regression

Original Windows-only baselines (2026-09-18): on the first cross-OS run all three visual tests failed on Ubuntu and macOS purely from font rendering (DirectWrite vs FreeType/CoreText), while Windows matched within tolerance; run-to-run noise on the same machine measured 0.0% changed pixels (max 4/255 delta in product images). The tests were `skipif` off Windows.

Per-OS baselines (2026-11-05): `visual/baselines/{win32,linux,darwin}/`. Linux and macOS sets were captured on the GitHub runners themselves ([run 42056097862](https://github.com/LSaiko/saucedemo-automation/actions/runs/42056097862), `update_baselines` dispatch) and reviewed by eye before commit. Cross-Python check on Linux: the five 3.11–3.15 captures were byte-identical except py3.11's inventory page, which differed in 239 pixels (0.017%), all under the 32/255 tolerance — 0% as far as the test counts. All 3 visual tests plus the `visual_user` xfail now pass on all 7 jobs.

## Not covered

`visual_user` on pages other than inventory (login/cart look identical for that persona).
