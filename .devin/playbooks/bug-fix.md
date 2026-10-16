# Bounded bug fix

Suggested cloud macro: !charging-bugfix

1. Confirm expected versus actual behavior and the specific synthetic reproduction.
2. Read the relevant routes, service/data logic, and existing tests. Run a baseline.
3. Add a regression test that fails for the reported reason, not a setup or import error.
4. Explain the suspected root cause and proposed minimal change. Ask before changing non-test code if the task requests a checkpoint.
5. Implement the authorized fix, preserving unrelated behavior and scope.
6. Run the regression, existing tests, lint, smoke, and dependency audit. Report pre-existing findings without hiding them.
7. Inspect the diff and explain allowed behavior, prohibited behavior, missing coverage, and limitations.
8. Prepare a PR if authorized. Stop for human review; do not merge or deploy.
