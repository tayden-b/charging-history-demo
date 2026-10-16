# Narrow migration

Suggested cloud macro: !charging-migrate

1. Confirm the reason for the migration and the behavior that must remain unchanged.
2. Inventory affected imports, callers, configuration, tests, and dependency constraints.
3. Run a baseline and read the upstream compatibility/migration guidance.
4. Choose one bounded slice. Explain what changes and how parity will be checked before implementation.
5. Update dependencies with the package manager and adjust only the necessary callers.
6. Verify request/response behavior, errors, uploads, and identity boundaries. Run the normal tests and CI-equivalent commands.
7. Report remaining warnings and failures honestly. Never silence deprecations instead of migrating, or relax security checks.
8. Describe review, rollout, and recovery considerations. Do not merge or deploy without approval.
