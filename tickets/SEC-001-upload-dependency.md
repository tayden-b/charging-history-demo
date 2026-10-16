# SEC-001: Upgrade the vulnerable charging-upload parser

## Source and scope

Synthetic remediation ticket backed by a real advisory, not a real Lucid finding. Target the primary application at this repository's current baseline. `python-multipart==0.0.17` is explicitly declared in pyproject.toml and used by the charging-history CSV upload endpoint.

Lead advisory: CVE-2024-53981 / GHSA-59g5-xgcq-4qw3.
https://github.com/advisories/GHSA-59g5-xgcq-4qw3

Malformed multipart boundaries can cause excessive per-byte processing/logging. The advisory's first fix is 0.0.18; that is historical context, not today's safe target. Run the current audit: newer advisories also affect this old package. Some findings depend on paths/options this app does not use; distinguish installed-version findings from confirmed applicability. Do not run resource-exhaustion payloads.

## Requested outcome

Update the upload parser to an appropriate compatible release that addresses the current known findings, without breaking legitimate CSV imports. Do not upgrade unrelated dependencies or claim every advisory is exploitable here.

## Acceptance criteria

- [ ] Record resolved versions, the direct/transitive path, baseline tests, and complete runtime audit.
- [ ] Check upstream advisory/release information and the release-age policy.
- [ ] Use the package manager; keep declaration and lockfile synchronized.
- [ ] Preserve valid upload behavior, exact money/energy units, identity attribution, atomic rejection, and request limits.
- [ ] Run upload tests, full suite, lint/format, smoke, and the same full runtime audit. Do not suppress findings.
- [ ] Inspect all dependency changes; explain any unexpected ones.
- [ ] Prepare a focused PR if authorized, with commands/results and unverified behavior.

No production deployment, auto-merge, or real credentials. If the audit cannot be made clean within scope, report what remains instead of weakening it. Owner and reviewer are training roles, not actual Lucid teams.
