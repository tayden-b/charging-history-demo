# Transitive dependency backup exercise

Independent test-only fixture for SEC-003. Do not serve or deploy it. TestClient runs it in process; no network listener or credentials are needed. It intentionally represents an older FastAPI dependency graph with Starlette resolved to 0.47.1. The primary app has a separate, newer graph.

Run these from the repository root:

```sh
uv sync --project practice/transitive --locked
uv run --project practice/transitive --locked pytest practice/transitive/test_exercise.py
uv tree --project practice/transitive --locked --invert --package starlette
```

For a full audit of this fixture, export its lockfile to the ignored operator area, then use the primary environment's scanner:

```sh
uv export --project practice/transitive --locked --no-dev --no-emit-project --no-hashes --output-file .local/transitive-requirements.txt
uv run --locked pip-audit --requirement .local/transitive-requirements.txt --no-deps --disable-pip
```

A nonzero audit is the intended starting point. Read every finding and the parent constraints. Do not use an advisory's historical first-patched version as a blanket security guarantee. Do not introduce overrides or change unrelated dependencies without explaining the compatibility implications.

This fixture's three tests check only a small HTTP contract. They do not demonstrate exploitability, large-upload concurrency safety, or production readiness. No stress payload is supplied.

Root CI deliberately checks the primary application; it does not certify this independent exercise. Publish or demonstrate this fixture only as an explicitly labeled backup scenario.
