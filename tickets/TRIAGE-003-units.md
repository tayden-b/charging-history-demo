# TRIAGE-003: Charging total appears one hundred times too large

## Report

Synthetic customer report: "The summary API returns `amount_minor: 1275` for Alice, but her two charging sessions cost $7.35 and $5.40. It should return 12.75. Please divide every stored amount by 100."

## Acceptance criteria

- [ ] Inspect the API schema, storage units, UI formatting, and tests.
- [ ] Reproduce the displayed value and establish expected versus actual behavior.
- [ ] Decide whether the report is an application bug, a contract misunderstanding, or a documentation gap, and explain the evidence.
- [ ] Do not change money representation, weaken assertions, or make a broad refactor just to satisfy an unverified request.
- [ ] Propose a bounded follow-up only if needed and agreed.

This is an intentionally ambiguous triage exercise. No code change is inherently required.
