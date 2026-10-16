---
name: repo-checks
description: Set up and verify ChargeLedger changes using the repository's actual tests, smoke check, and dependency audit.
---

1. Read AGENTS.md and the assigned ticket. Confirm the repository root and branch.
2. Use Python 3.12 and uv 0.9.28. Run `uv sync --locked`; do not relax the release cutoff.
3. Run `uv run --locked pytest` and record the baseline, including warnings and failures.
4. Inspect which tests exercise the affected behavior. Do not treat a green baseline as complete coverage.
5. After an authorized change, run `uv run --locked ruff check .`, `uv run --locked ruff format --check .`, `uv run --locked pytest`, and `uv run --locked python -m scripts.smoke`.
6. Run `uv run --locked python -m scripts.audit`. Preserve the raw JSON and the nonzero status on vulnerable baselines. Never ignore findings or modify checks to obtain green output.
7. If browser validation is useful, run `uv run python -m app` on localhost and use only synthetic data.
8. Report exact commands, results, limitations, and any remaining findings. Stop before merge or deployment.
