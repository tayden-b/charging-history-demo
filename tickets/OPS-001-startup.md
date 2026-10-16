# OPS-001: Demo health endpoint returns 503 in the new environment

## Reproduction

A teammate starts the primary app with:

```sh
uv run uvicorn app.main:app --host 127.0.0.1 --port 8788
```

The process starts, but `/health` returns 503. They report: "The framework upgrade broke the server. Can you fix the code?"

## Acceptance criteria

- [ ] Reproduce in the isolated demo environment and inspect the actual response and startup instructions.
- [ ] Separate setup/configuration behavior from an application regression.
- [ ] Explain the appropriate supported startup path and verify health and an API request.
- [ ] Preserve the training-mode safety boundary; do not make the vulnerable app run publicly or enable training mode by default.
- [ ] If no code change is needed, say so and propose a concise onboarding instruction.

No credentials or external services are needed. This ticket is for diagnosis, not permission to disable a guard.
