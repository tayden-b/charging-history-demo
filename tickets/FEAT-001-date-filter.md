# FEAT-001: Filter charging history and totals by date range

## Customer request

"I want to look at a period of charging history without downloading everything. The totals should match the records I am looking at."

Clarify the API contract before coding. Proposed starting point: optional `from_date` and `to_date` parameters on the history and summary endpoints, expressed as ISO dates, inclusive in UTC. Decide explicitly how invalid dates, reversed ranges, empty results, and omitted bounds behave.

## Acceptance criteria

- [ ] Agree the exact behavior and identify affected callers.
- [ ] History and summary apply the same date-range semantics without duplicating filtering logic.
- [ ] User scoping remains enforced and behavior without filters stays compatible.
- [ ] Add boundary tests covering midnight, both bounds, one bound, empty results, and invalid inputs.
- [ ] Update the API description and, only if agreed, the browser interface.
- [ ] Run normal verification and prepare a bounded reviewable change.

Do not turn this into a new database, authentication system, charting dashboard, or broad refactor. Existing remediation tickets remain separate work.
