# TEST-001: Verify request-size controls without a Content-Length header

## Customer concern

"Our request-size tests cover ordinary uploads, but clients can stream a body without declaring its length. Do we actually enforce the limit while receiving data?"

The app documents a 512 KiB total-request limit and a 256 KiB file limit. Existing tests do not cover every ASGI receive pattern.

## Acceptance criteria

- [ ] Inspect the existing middleware and tests before choosing new cases.
- [ ] Add bounded tests for a body split into chunks with no Content-Length, exactly at the request limit, above it, and an early disconnect.
- [ ] Assert the observed status/response and whether the downstream app was invoked; do not rely only on internal implementation details.
- [ ] Keep tests small and deterministic; no live denial-of-service or load test.
- [ ] If a production-code change appears necessary, explain the failing behavior and proposed scope before changing it.
- [ ] Run the existing suite and report what the tests do not establish.

The objective is meaningful coverage. Do not claim the entire application is secure because these cases pass.
