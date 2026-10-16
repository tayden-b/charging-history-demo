# Small feature with a customer

Suggested cloud macro: !charging-feature

1. Restate the desired user outcome and clarify observable acceptance criteria.
2. Map the request through the API, data operations, and UI only where necessary.
3. Run baseline checks and identify one small implementation slice.
4. Agree the public API behavior, validation errors, identity boundaries, and what remains out of scope.
5. Add meaningful tests and implement the agreed slice without unrelated refactors.
6. Run the repository checks and inspect the actual diff and output.
7. Update the API contract/documentation if the behavior changed. Report remaining work and stop for review.
