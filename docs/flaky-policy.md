# Flaky test policy

Every test is retried up to **2 times, 3 seconds apart**, before it counts as a failure (`--reruns 2 --reruns-delay 3` in `pytest.ini`, via [pytest-rerunfailures](https://github.com/pytest-dev/pytest-rerunfailures)). Tests marked `@pytest.mark.no_rerun` are never retried.

## Flaky vs broken

| | Flaky | Broken |
|---|---|---|
| Pattern | Fails, then passes on a retry with no code change | Fails on every attempt |
| Typical cause | Timing: page not settled, network jitter to saucedemo.com, slow CI runner, Chrome/driver startup hiccup | Real regression in the site, a wrong locator, a wrong assertion |
| What the run does | Passes; reported as **flaky** | Fails after 3 attempts |
| What you do | Treat it as a bug in the *test* and fix it (usually a missing explicit wait). A retry buys time. It is not a fix. | Investigate as a normal failure |

A test that is flaky across several CI runs gets fixed or quarantined. The retry is there so one timing blip doesn't turn the 7-job matrix red. It shouldn't hide a test that fails half the time.

## Where it shows up

- **Terminal**: rerun attempts show as `R`, and a pass after a retry shows as `f` / `FLAKY`. The summary line reads e.g. `36 passed, 1 rerun, 1 flaky`.
- **HTML report** (`reports/report.html`): each failed attempt gets its own **Rerun** row, with the failure screenshot attached. The final passing row has a **Flaky** column entry, e.g. `flaky (passed on attempt 2)`. The Result column still says Passed, so pytest-html's filters and counts keep working.

## Why 2 reruns

- **Not 0**: this suite drives a live third-party site through a real headless Chrome on shared CI runners. Occasional timing failures that have nothing to do with the code are a fact of life. With no retries, the matrix would regularly fail for no real reason, and people would learn to ignore red builds.
- **Not 5**: every rerun hides signal and costs time. A genuinely broken test burns (1 + reruns) × test duration + reruns × 3s before it's reported. That's about 3× at 2 reruns and 6× at 5. At 5 reruns, a test that fails 80% of the time still passes most runs (1 − 0.8⁶ ≈ 74%), which amounts to a real bug going unreported. At 2, it passes about half the time (1 − 0.8³ ≈ 49%), and the flaky label makes it visible.
- **Why 2 and not 1**: one retry is enough for a single blip. The second retry covers a blip that repeats on the next attempt, such as a CI runner that stays slow for a few seconds. The 3s delay gives the runner or site time to recover instead of retrying immediately.

## Excluded: `@pytest.mark.no_rerun`

For these tests, a first-try failure is always trusted as a real bug:

| Tests | Why |
|---|---|
| `test_login.py`: `test_locked_out_user`, `test_wrong_password`, `test_empty_fields`, `test_empty_password` | Explicit validation-error assertions. The error banner is rendered synchronously by client-side validation, with no network wait and no animation, so a timing-caused failure isn't plausible. If the wrong message (or none) appears, the validation rule changed. |
| `test_checkout.py`: `test_missing_first_name_shows_error`, `test_missing_field_shows_error` (both params) | Same reasoning, for checkout form validation. A retry here would only mask a changed or missing validation rule. |

Not excluded, but not retried either: `xfail(strict=True)` tests (known site bugs). pytest-rerunfailures doesn't retry expected failures, and if an xfail test unexpectedly passes, that's a strict failure and isn't retried.

To add a test to the list, put `@pytest.mark.no_rerun` on it. The only rule is that its failure must never be explainable by timing. `conftest.py` turns the marker into `flaky(reruns=0)`, pytest-rerunfailures' own per-test override. To opt out globally for a debugging run, use `pytest --reruns 0`.
