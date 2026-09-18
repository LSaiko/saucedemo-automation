# Functionality test plan — results

**Date:** 2026-09-18 · **Commit:** `17609c6` · **CI:** [run 35319814885](https://github.com/LSaiko/saucedemo-automation/actions/runs/35319814885) (headless Chrome, 7-job matrix)

**36 tests: 32 passed, 4 xfailed (known site bugs), 0 failed — 98s** on windows-latest (local Windows run: same result, 95s). Linux/macOS jobs: 29 passed, 3 skipped (visual tests are Windows-only, see below), 4 xfailed — 47s.

Test cases are defined in [test-cases.md](test-cases.md).

| Area | Cases | Pass | Known bug (xfail) | Notes |
|---|---|---|---|---|
| Login | L1–L6 | 6 | – | valid, locked-out, wrong pw, empty user, empty pw, performance_glitch |
| Inventory | I1–I6 | 6 | – | add/remove badge, sort A–Z/Z–A/price ↑↓, item detail + back, logout |
| Cart | C1–C4 | 4 | – | contents, remove, continue shopping keeps cart, empty-cart checkout allowed |
| Checkout | K1–K6 | 7 | – | totals verified (subtotal = Σ prices, total = subtotal + tax), first/last/zip validation, cancel from step one/overview, back-home clears cart |
| Personas | P1–P6 | 6 | 4 | see defects below |
| Visual | V1–V3 | 3 | – | login, inventory, cart-with-items screenshots vs committed baselines; ≤2% pixel change, 32/255 per-channel tolerance |

## Site defects found

All are pre-existing, intentional saucedemo demo behaviour. Each is marked `xfail(strict=True)` with a screenshot of the broken state attached to `reports/report.html`; the test turns red if saucedemo ever fixes it.

1. `problem_user` — sort dropdown has no effect (P3)
2. `problem_user` — checkout last-name input discards keystrokes (P4)
3. `error_user` — sorting raises a "Sorting is broken!" alert (P5)
4. `error_user` — Finish does not complete the order (P6)
5. Any user — an empty cart can proceed to checkout step one (C4, asserted as current behaviour, not xfail)

No fixes required on the suite side: the defects are in the application under test.

## Stability

Two transient `TimeoutException`s (cold Chrome start + slow first page load) seen during initial development; resolved by raising the base explicit wait from 10s to 15s. Zero flakes since across ~10 local and 3 CI runs.

## Visual regression

Baselines were captured on Windows 11 / headless Chrome at 1280×900 and committed. On the first cross-OS run all three visual tests failed on Ubuntu and macOS purely from font rendering (DirectWrite vs FreeType/CoreText), while Windows matched within tolerance; run-to-run noise on the same machine measured 0.0% changed pixels (max 4/255 delta in product images). The tests are therefore `skipif` off Windows; per-OS baselines are the follow-up (see TODO.md).

## Not covered

`visual_user` layout defects — the pixel-diff tooling now exists; a `visual_user` login compared against the `standard_user` baselines is the remaining step.
