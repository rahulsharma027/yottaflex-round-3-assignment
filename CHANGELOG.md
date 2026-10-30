# Changelog

## Unreleased

## 1.1.0 — 2026-10-30

### Added

- First-run login guide with the recommended administrator username, password-location/reprint instructions, role explanations and username shortcuts.
- Interactive summary cards filter and smoothly scroll to the queue, with selected-state feedback, live result announcements and normal GET fallbacks.

### Changed

- Reviewers default to current Assigned to me cases, newest opening date first; assignment scope is separate from sorting and retained across filters, pagination and case return links.
- Case files now lead with student details and full original submitted text, followed by evidence, response, decisions and dated timeline, with section navigation and actions alongside.
- Clear account/password placeholders and sign-in progress text; smaller-screen visitors see the guide before focusing a field.
- Already-authenticated visitors to the login page return to their workspace.

### Fixed

- Assigned to me and All cases now switch immediately; the separate status-reset tab is labelled All statuses.
- Assignment-scope controls appear only for reviewers; administrator, support and learner queues omit irrelevant Assigned to me controls and ignore stale assignment-scope URLs.

Verification: all 31 automated tests pass on Python 3.14.10; role-specific queues and case files were inspected at desktop and phone sizes, with case files also checked at tablet size. See [verification details](docs/VERIFICATION.md). No database migration or local-data reset is required; restart the launcher and refresh the browser to load the updated interface.

## 1.0.0 — 2026-10-30

Initial working baseline of **ACI (Academic Integrity) Portal By Yotta**, preserved by the annotated Git tag `v1.0.0`.

- Responsive case workspace with search, filters, pagination, evidence, decisions, appeals, policy and evaluation screens.
- Server-enforced roles, learner ownership, reviewer eligibility/conflicts, independent appeals, transactional audit history and stale-action protection.
- One-command local Django/SQLite setup with generated credentials and non-destructive subsequent launches.
- Deterministic full dataset: 10,000 submissions, 1,000 flags and 300 cases; CSV/JSON/SQL exports, separate ground truth, four isolated negative fixtures and matching two-run checksums.
- Architecture, schema, assumptions, reviewer walkthrough, requirement traceability, AI-use disclosure and recorded verification.

Verification for this baseline includes 26 automated checks on Python 3.14.10 and 3.15.1, clean-clone setup, and desktop/phone/tablet inspection. See [the verification record](docs/VERIFICATION.md) for exact scope and limitations. This tag records the current implementation, not completion of candidate personal review or portal submission.

Interface and workflow improvements will be recorded in subsequent versions without changing this baseline tag.
