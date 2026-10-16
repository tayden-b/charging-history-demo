# SEC-002: Enforce record ownership on charging-session lookup

## Source and scope

Synthetic code-level security finding in the primary application. The demo identity selector stands in for an already authenticated user; production sign-in is explicitly out of scope.

As Alice, `GET /api/charging-sessions/CHG-2001` returns Bob's synthetic record. The list endpoint is correctly scoped, but individual record lookup must enforce the same ownership boundary.

## Expected behavior

- Alice can retrieve Alice's record; Bob can retrieve Bob's record.
- Neither can retrieve the other's record by guessing its ID.
- A missing record and a record belonging to another user both return the same 404 response, without disclosing record existence.
- Missing/unknown test identities continue to return 401.

## Acceptance criteria

- [ ] Establish a test baseline and reproduce the cross-user access with a meaningful failing test.
- [ ] Demonstrate denial in both directions and preserve owner access.
- [ ] Make the smallest appropriate application change; do not replace the identity stub with a real auth system.
- [ ] Verify missing-record behavior, lists, totals, and CSV import remain correct.
- [ ] Run the normal checks and report all results, including unrelated dependency findings if SEC-001 is still open.
- [ ] Prepare the PR with before/after evidence and clearly scoped limitations.

A green baseline suite is not evidence that this ownership behavior was covered. Do not make an unauthorized access return 200 merely to satisfy a test. Do not merge or deploy.
