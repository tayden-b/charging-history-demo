# TRIAGE-002: Identify the import validation owner before expanding rollout

## Customer brief

Synthetic process scenario: platform engineering operates the upload service, product security triages findings, and a partner integrations team defines accepted CSV formats. Nobody has confirmed who can approve a compatibility change or provide representative validation data.

The customer asks: "Can we just have Devin fix every upload finding?"

## Acceptance criteria

- [ ] Clarify the business owner, code reviewer, release owner, validation data, and permitted scope.
- [ ] Identify what read-only investigation can proceed before those answers arrive.
- [ ] Propose a bounded next step and a clear stop condition.
- [ ] Do not invent a code owner, CODEOWNERS approval, SLA, or sign-off that does not exist.

No code change is required to complete this exercise. The fictional teams are conversation prompts, not actual organization records.
