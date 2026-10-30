# Development log

## 2026-10-30 — implementation session

Reviewed AGENTS.md, challenge notes, assignment breakdown, reusable project prompt, reviewer experience, prompt history, and the existing Yotta remote. Original attachment files were not present; used their recorded interpretation and stated that limit. Copied supporting documentation into this repository so a reviewer needs no parent-folder files. Parent copies remain as preparation history.

Components built in dependency order:

1. Django/SQLite foundation: pinned dependencies, isolated launcher, ignored configuration and local credentials.
2. Relational schema: ten core entities, protected keys, assignments/conflicts, explicit decision-evidence bridge, immutable evidence versions, timeline, triage actor records, optimistic counters and submission receipts. Generated migrations and field dictionary.
3. Transactional workflow: scoped roles, explicit human triage, reviewer eligibility/reassignment, notice/response, evidence, decisions, independent appeals and closure. Stale actions and unsupported findings are rejected.
4. Deterministic data: starter/full modes, fixed seed/dates/IDs, scenario-derived outcomes, CSV/JSON/SQL, separate truth and four isolated exceptions.
5. Validation: structural/arithmetic/date/lifecycle/audit checks, anomaly detection before truth join, formulas, two-run hashes, packaged exports and actual proof.
6. Custom interface: forest/cream institutional ledger; queue, filtering/search/pagination, submission/report, case evidence/decision/timeline, role-aware action panels, policy, guide and restricted evaluation view. Local assets and progressive enhancement.
7. Verification and refinement: workflow/data tests, desktop/phone/tablet inspection, mobile menu/cards, readable annotations, retained form input/errors, clean setup/preservation/reset checks, supported-runtime test and source cleanup.
8. Documentation: architecture/ERD/lifecycle/permissions, data dictionary, scenario/provenance/metric explanation, walkthrough, requirement traceability, real verification and explicit AI-use limits.

Final review caught reviewer profiles without a corresponding demo login. All six reviewer profiles now receive accounts, and live assignment/decision eligibility rejects inactive or missing accounts. A regression check verifies inactive-account rejection. Development-only Prettier formatting makes the CSS/JavaScript readable without adding a reviewer runtime requirement.

Meaningful local commits group workflow/interface, data/tests/proof, and documentation/refinement. They use actual current timestamps. They are not backdated scenario history. No push, deployment or portal submission is implied.

## Decisions Rahul should understand

- Why a report flag is different from case state and decision outcome.
- Why services check permissions even when a button is hidden.
- Why case changes and audit entries share a transaction and a version claim.
- Why evidence corrections append records and decisions retain original evidence references.
- Why appeal independence covers every past original reviewer.
- Why truth is not stored in operational models, and why detection runs before joining labels.
- How fixed seed, source dates, ordering, encoding and counters produce identical exports.
- Why SQLite/Django templates make clone-and-run small, and where production boundaries begin.

## Remaining handoff work

Candidate must personally review, run and explain the implementation, and record that honestly. Reconcile the partial prompt record with complete exports from every AI tool used and compare requirements against original attachments. The local implementation has not been pushed; publish the reviewed local commits before portal submission. Verify the public remote after publication, then submit its URL under the invitation's instructions before the deadline. See VERIFICATION.md for exact platform/testing limitations.

## 2026-10-30 — portal branding

User selected **ACI (Academic Integrity) Portal By Yotta**. A shared brand template now supplies the sidebar and login identity, with the expanded name in accessible labels/browser metadata/footer, and matching launcher/README display text. Existing technical paths remain stable. Django checks and the existing page-render test passed; desktop (1440×1000) and phone (375×812) branding were inspected. Refreshed the README desktop screenshot and added a phone branding screenshot; earlier workflow screenshots remain historical verification evidence.
