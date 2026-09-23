# Flaky test policy

Every test gets up to **2 reruns with a 3-second delay** (`--reruns 2 --reruns-delay 3` in `pytest.ini`, via pytest-rerunfailures), except tests marked `@pytest.mark.no_rerun`.

## Flaky vs broken

- **Flaky**: same code, same test, different outcome. It failed at least once and then passed on a retry. Typical causes: saucedemo.com responding slowly, a Chrome/driver hiccup, an element rendered a moment after a wait gave up. Each attempt gets a fresh browser (the `driver` fixture is function-scoped), so a retry does not inherit a broken session.
- **Broken**: fails on all 3 attempts. That is a real failure (a site change, a regression or a bad test) and the run goes red.

A flaky result still needs fixing. It means the test depends on timing it shouldn't. The fix is usually a missing explicit wait in the Page Object, not more reruns.

## Where flakes show up

- Terminal summary: `31 passed, 1 flaky, 1 rerun`. A passed-after-retry test is counted as `flaky`, not `passed`
- HTML report (`reports/report.html`): a **Flaky** column reading `FLAKY: passed on attempt N`, plus one **Rerun** row per failed attempt with its screenshot and URL. The "Reruns" filter checkbox shows only those rows

Debug locally without retries: `pytest --reruns 0` (a later CLI flag overrides `addopts`).

## Why 2 reruns

The decision rests on two numbers: how often a transient failure still goes red, and how often a real intermittent bug gets hidden. Assume attempts are independent and a test fails with probability `p` per attempt:

| Reruns | Transient flake, p = 5%: run goes red | Real race bug, p = 50%: run goes red | Cost of a broken test |
|---|---|---|---|
| 0 | 5% | 50% | 1 attempt |
| **2** | **0.0125%** | **12.5%** | **3 attempts + 6 s** |
| 5 | ~0% | 1.6% | 6 attempts + 15 s |

- **Not 0**: the suite runs 37 tests on 7 CI jobs against a public site we don't control. A 5% per-test network blip makes almost every CI run red for reasons unrelated to the code, and people learn to ignore red builds
- **Not 5**: a genuine race condition that fails half the time would go red in only 1.6% of runs. That's effectively hidden. Each broken test would also cost 6 browser sessions plus 15 s of delay per CI job
- **2** removes nearly all transient noise while still going red on a 50/50 bug in 1 run out of 8. It also shows as flaky in the report every time it needed a retry

The 3-second delay lets a slow page load or a brief network error clear before the next attempt. Retrying immediately tends to hit the same problem again.

## Excluded: `@pytest.mark.no_rerun`

Tests with this marker get `flaky(reruns=0)` from `conftest.py`, which overrides the global default. Their first failure is final.

Currently excluded are the **explicit validation-error assertions**:

- `tests/test_login.py`: `test_locked_out_user`, `test_wrong_password`, `test_empty_fields`, `test_empty_password`
- `tests/test_checkout.py`: `test_missing_first_name_shows_error`, `test_missing_field_shows_error`

Why these are excluded:

- The error banner is rendered client-side, synchronously, on submit. There's no network round trip and no animation to race, and the Page Object's explicit wait already covers rendering. There is no plausible transient cause
- When one fails, either the message text changed or validation didn't fire. Both are real bugs. A retry would only fail the same way, adding 6 s per test
- A retry that *passes* would be worse. Validation that fires only sometimes is a genuine defect in input handling, and a rerun would report it as green

When adding a test, use `no_rerun` if the assertion checks deterministic behaviour that doesn't depend on network or timing. Leave it off for anything that loads pages, waits on navigation or takes screenshots. The visual regression tests are not excluded, because a screenshot taken before fonts or images finish loading is a transient failure. A real visual regression still fails all 3 attempts.
