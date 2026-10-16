# SEC-003: Investigate the transitive upload framework advisory

## Source and scope

Backup exercise only. Work in `practice/transitive`, which has its own manifest, lockfile, tests, and environment. This is not a claim that the primary application's current Starlette version is vulnerable.

A legacy FastAPI upload service has a lockfile resolving Starlette 0.47.1. The application did not declare Starlette as a direct dependency. Its dependency audit flags upload-related advisories, including:

CVE-2025-54121 / GHSA-2c2j-9gv5-cj73
https://github.com/advisories/GHSA-2c2j-9gv5-cj73

The advisory concerns file uploads blocking the event-processing thread during rollover to disk. The historical first fix is 0.47.2. Check current advisories and parent constraints rather than assuming that version is sufficient today.

## Acceptance criteria

- [ ] Identify which parent brings Starlette in and the versions that parent allows.
- [ ] Run the fixture's tests and complete runtime audit before changing anything.
- [ ] Propose a compatible fix. If the parent must change, explain that before proceeding.
- [ ] Update only the backup fixture's dependency declarations/lockfile and necessary fixture code.
- [ ] Preserve the upload/health response contract, validate the full scoped audit, and disclose compatibility concerns.
- [ ] Do not modify the primary application's dependencies or weaken the fixture audit.

No large stress payloads. Parent upgrades require explicit scope agreement. A version-only scanner finding is not by itself proof of application exploitability.
