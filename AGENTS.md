# ChargeLedger agent instructions

This is an intentionally vulnerable, synthetic training application. It is not Lucid code or a production service. No real identities, credentials, VINs, locations, or customer data belong here. Run only in an isolated local/cloud development environment; never deploy publicly.

## Scope

Work only on the assigned ticket. The initial upload dependency and record-detail ownership behavior are deliberate exercise baselines. Do not silently fix other tickets. The X-Demo-User selector simulates an authenticated identity; real sign-in is out of scope.

Never weaken checks, ignore advisories, disable branch protections, bypass hooks, or add skipped/xfail tests to achieve green output. Do not edit GitHub workflows or this file as part of a remediation unless explicitly requested. Never merge, publish, deploy, launch paid sessions, or change access without approval.

## Environment

Use Python 3.12 and uv 0.9.28. Run `uv sync --locked` from the repository root. The release cutoff in pyproject.toml is intentional. Do not relax it to resolve dependency errors. No database, credentials, Docker, or external API is needed for the primary application.

`uv run python -m app` starts the local-only demo on 127.0.0.1:8787. The launcher enables the explicit training mode. All records are in memory; restarting discards imports and restores the synthetic seed.

## Verification

- Lint: `uv run --locked ruff check .`
- Format check: `uv run --locked ruff format --check .`
- Tests: `uv run --locked pytest`
- Smoke: `uv run --locked python -m scripts.smoke`
- Runtime dependency audit: `uv run --locked python -m scripts.audit`

Run the baseline before edits. The initial audit intentionally returns nonzero; that is a real finding, not a reason to disable the gate. The audit covers the complete locked runtime graph for the primary application, not the dev tools or separate transitive exercise. Inspect raw results; alias records can refer to the same CVE.

Tests must check behavior, not dependency version strings. Add a regression that fails for the relevant reason before a code fix, then verify it passes afterward. A green baseline suite does not imply sufficient security coverage. Report warnings and missing checks.

## Code conventions

Keep API wiring in app/main.py, parsing in app/imports.py, models in app/models.py, and data operations in app/store.py. Use integer cents and watt-hours. CSV imports are atomic and user-scoped. No external services or unnecessary abstractions.

## PR handoff

Link the ticket. State the baseline commit, changes, advisory/compatibility reasoning where applicable, exact commands/results, test coverage, and unverified behavior. No PR opened/green/merged status means deployed. Stop for human review.

## Practice

Tickets are in tickets/index.json and corresponding Markdown files. They are inputs, not proof of execution. practice/transitive is an independent backup exercise, not part of the primary application's runtime. .local is ignored operator material; do not use it as an answer key unless the user asks.
