# MIG-001: Migrate the deprecated HTTP test-client integration

## Observed behavior

The primary application's baseline tests emit a Starlette deprecation warning about using the legacy `httpx` test-client integration and recommend `httpx2`. Tests currently pass; this is not a failing feature.

## Requested outcome

Investigate and migrate the test-client setup to a supported path, maintaining behavior and the established dependency release-age policy. Read the current upstream migration guidance first. Do not assume the replacement has identical APIs or that the newest release is appropriate.

## Acceptance criteria

- [ ] Capture baseline tests and the exact warning.
- [ ] Inventory affected imports, dependency declarations, and callers.
- [ ] Explain the proposed dependency/API changes and compatibility checks before implementation.
- [ ] Keep the change limited to tooling unless a necessary application change is explicitly agreed.
- [ ] Verify request/response behavior, headers, multipart uploads, error handling, and smoke tests.
- [ ] Remove the warning through migration, not filters or suppression.
- [ ] Run normal checks, report unrelated existing advisory findings, and describe recovery by reverting the reviewed change.

This is a narrow migration exercise, not a prediction of the onsite task. Do not upgrade the entire project opportunistically.
