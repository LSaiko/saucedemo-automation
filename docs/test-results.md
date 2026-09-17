# Functionality test plan — results

**Date:** 2026-09-17 · **Commit:** `c80c324` · **CI:** [run 35177403705](https://github.com/LSaiko/saucedemo-automation/actions/runs/35177403705) (ubuntu-latest, headless Chrome)

**33 tests: 29 passed, 4 xfailed (known site bugs), 0 failed — 73s** (local Windows run: same result, 130s)

Test cases are defined in [test-cases.md](test-cases.md).

| Area | Cases | Pass | Known bug (xfail) | Notes |
|---|---|---|---|---|
| Login | L1–L6 | 6 | – | valid, locked-out, wrong pw, empty user, empty pw, performance_glitch |
| Inventory | I1–I6 | 6 | – | add/remove badge, sort A–Z/Z–A/price ↑↓, item detail + back, logout |
| Cart | C1–C4 | 4 | – | contents, remove, continue shopping keeps cart, empty-cart checkout allowed |
| Checkout | K1–K6 | 7 | – | totals verified (subtotal = Σ prices, total = subtotal + tax), first/last/zip validation, cancel from step one/overview, back-home clears cart |
| Personas | P1–P6 | 6 | 4 | see defects below |

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

## Not covered

`visual_user` layout defects — require pixel-diff/visual testing tooling.
