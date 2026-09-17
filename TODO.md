# What's left

## Done
- [x] Manual walkthrough + test cases (`docs/test-cases.md`)
- [x] Page Objects, driver fixture, tests (33: 29 pass, 4 xfail)
- [x] pytest-html with screenshot-on-failure/xfail
- [x] README, results (`docs/test-results.md`)
- [x] Pushed to GitHub, CI green on every push
- [x] Chrome installed locally
- [x] Parallel runs via pytest-xdist (`-n auto`): ~60s local, ~56s CI

## Manual
- [ ] Pin the repo on your GitHub profile (no API for this): github.com/LSaiko → "Customize your pins" → `saucedemo-automation`

## Optional / when needed
- [ ] `visual_user` layout checks — needs a visual-diff tool (e.g. `pytest-playwright` snapshots or Applitools)
- [ ] Move credentials to `.env` (gitignored) if real accounts are ever used; saucedemo's public ones are fine hardcoded
- [ ] Python-version / OS matrix in CI if you target more than one runtime
- [ ] Bump `actions/*` versions when GitHub drops Node 20 runners (currently a warning only)
