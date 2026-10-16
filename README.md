# ChargeLedger: remediation practice

A small Python charging-history API with a local browser interface, synthetic users, CSV import, automated tests, and GitHub Actions. It is a representative cloud-service demo, not Lucid's code or an official interview assignment.

## Safety and initial state

This is an intentionally vulnerable training fixture, not a deployable product:

- The upload parser is deliberately pinned to a version with real published advisories.
- The record-detail endpoint has a deliberate ownership-check gap. The existing tests do not establish cross-user detail isolation.
- `X-Demo-User` is a fake identity selector, not production authentication. Everyone can choose either synthetic identity.
- No real data, credentials, public deployment, or live attack/stress test is needed.
- The launcher binds to localhost. Direct ASGI startup is disabled unless `CHARGING_DEMO=1` is explicitly set. Host restrictions and request caps reduce accidental exposure, but do not turn this into a safe public service.

Do not silently remediate the baseline before the learner's session. Do not weaken CI to hide the findings.

## Run locally

Requires Python 3.12 and uv 0.9.28 (already used to generate the lockfile).

```sh
uv sync --locked
uv run python -m app
```

Open http://127.0.0.1:8787. Stop with Ctrl+C. Change the port with `uv run python -m app --port 8788`.

No database, Docker, real identity provider, API keys, or paid Devin sessions are required to run this application. Data lives in memory. Restarting restores the seed and discards any imported records.

Select Alice or Bob, inspect a record, or upload `examples/charging-upload.csv`. The interface shows real API responses and installed dependency versions, not a simulated security score.

## Validate

```sh
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked pytest
uv run --locked python -m scripts.smoke
uv run --locked python -m scripts.audit
```

The initial functional suite and smoke check should pass. The dependency audit should fail on the intentionally vulnerable upload parser. Read `artifacts/dependency-audit.json`; do not ignore findings to make it pass. Multiple advisory identifiers may alias the same vulnerability. The scan is based on the locked runtime graph, not merely direct dependencies; dev tools and the separate backup exercise are not in that scope. A scan service/network failure is not a clean scan.

## API

Data endpoints require `X-Demo-User: alice` or `X-Demo-User: bob`.

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/health` | Startup health and training mode |
| GET | `/api/demo/context` | Synthetic identities and installed versions |
| GET | `/api/charging-sessions` | Selected user's history |
| GET | `/api/charging-sessions/{session_id}` | Individual record (see SEC-002) |
| GET | `/api/summary` | Selected user's integer-unit totals |
| POST | `/api/imports/csv` | Multipart `file` field containing CSV |
| GET | `/examples/charging-upload.csv` | Synthetic sample upload |
| GET | `/openapi.json` | API schema |

CSV columns, in order: `session_id,charged_at,energy_kwh,amount_usd`. Times must include a timezone. Amounts allow two decimal places; energy allows three. Maximum 100 rows, 256 KiB file, 512 KiB total request. Validation or duplicate-ID failure imports nothing. Uploaded records belong to the selected test identity.

## Repository map

```text
app/main.py                API routes and app composition
app/store.py               Per-app in-memory data, scoped lists, atomic imports
app/imports.py             CSV validation and unit conversion
app/middleware.py          Explicit training gate and request limits
app/static/                Small browser interface, no frontend build
examples/                  Synthetic upload fixtures
tests/                     Existing application behavior tests
scripts/audit.py           Locked-runtime advisory scan, preserves exit status
scripts/smoke.py           Startup/UI/import verification
scripts/tickets.py         Local issue-payload preview; no GitHub writes
.github/workflows/ci.yml    Four independent PR checks
.devin/skills/repo-checks/  Repeatable setup and verification instructions
.devin/playbooks/          Copyable, reviewable workflow prompts
practice/transitive/       Separate backup dependency exercise
```

## Demo and practice tickets

Start with `tickets/index.json`. SEC-001 and SEC-002 are the two main demo tasks. The remaining tickets cover transitive dependency investigation, duplicate triage, owner/acceptance clarification, a feature, test coverage, a narrow tooling migration, and a setup incident. They are not all vulnerabilities or tasks to fix at once.

```sh
uv run python -m scripts.tickets
uv run python -m scripts.tickets SEC-001
```

The second command prints a GitHub issue payload for review; it never creates an issue. Only publish tickets or connect a remote after approval. No actual GitHub issues or PRs are created by this local scaffold.

## GitHub Actions and review

On PRs, pushes to main, and manual dispatch, `.github/workflows/ci.yml` runs four named checks: Lint, Tests, Application smoke, Dependency audit. Test/audit artifacts are preserved on failure. There is no deployment, auto-merge, paid-agent trigger, or stored credential in CI. Third-party actions are pinned to verified commit SHAs; uv and direct packages are version-pinned and the lockfile is committed when publishing.

Running CI is not the same as requiring it. After publication, a human must configure required checks and reviewer rules if the GitHub plan supports them, confirm the Devin identity has no bypass, and verify actual runs. None of those remote controls are configured locally.

For the cleanest demonstration, remediate SEC-001 first. After a human accepts that change, address SEC-002 on the updated baseline so the unrelated dependency finding does not obscure the code-fix checks. No merge needs to happen live. Describe prepared artifacts honestly; an open PR, a green check, or a merged change is not a deployed fix.

## Repeatable workflows

`.devin/playbooks/dependency-remediation.md` is the primary playbook draft. The bug-fix, feature, and migration drafts support practice. These files are not automatically installed cloud playbooks. Refine them from real completed runs, then create the corresponding playbooks in the permitted Devin organization. The repository skill is available to agents that discover `.devin/skills/`.

To reset practice, prefer a fresh branch/worktree from a saved baseline. Do not discard uncommitted work, force-push, or reset shared branches. The local server restart resets data only, not code or dependencies.

## Limits

There is no real sign-in, persistent database, production authorization infrastructure, external scanner integration, Jira integration, deployment, or fleet-wide proof. GitHub is the deliberate stand-in for the scenario's GitLab/Jira setup. The framework may emit a test-client deprecation warning; MIG-001 is an optional migration exercise, not a reason to suppress warnings.
