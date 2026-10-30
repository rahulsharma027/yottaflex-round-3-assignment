# Changelog

## Unreleased

- First-run login guide with the recommended administrator username, exact password-location/reprint instructions, role explanations and username shortcuts.
- Clear account/password placeholders and sign-in progress text; smaller-screen visitors see the guide before focusing a field.
- Already-authenticated visitors to the login page return to their workspace.

## 1.0.0 — 2026-10-30

Initial working baseline of **ACI (Academic Integrity) Portal By Yotta**, preserved by the annotated Git tag `v1.0.0`.

- Responsive case workspace with search, filters, pagination, evidence, decisions, appeals, policy and evaluation screens.
- Server-enforced roles, learner ownership, reviewer eligibility/conflicts, independent appeals, transactional audit history and stale-action protection.
- One-command local Django/SQLite setup with generated credentials and non-destructive subsequent launches.
- Deterministic full dataset: 10,000 submissions, 1,000 flags and 300 cases; CSV/JSON/SQL exports, separate ground truth, four isolated negative fixtures and matching two-run checksums.
- Architecture, schema, assumptions, reviewer walkthrough, requirement traceability, AI-use disclosure and recorded verification.

Verification for this baseline includes 26 automated checks on Python 3.14.10 and 3.15.1, clean-clone setup, and desktop/phone/tablet inspection. See [the verification record](docs/VERIFICATION.md) for exact scope and limitations. This tag records the current implementation, not completion of candidate personal review or portal submission.

Interface and workflow improvements will be recorded in subsequent versions without changing this baseline tag.
