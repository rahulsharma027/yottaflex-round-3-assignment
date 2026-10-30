# Development log

## Version 1 baseline

The user requested preserving the current implementation as version 1 before further interface and workflow enhancements. `CHANGELOG.md` and the annotated `v1.0.0` Git tag identify this baseline. Subsequent improvements should preserve the tag and receive their own commits/version notes.

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

Candidate must personally review, run and explain the implementation, and record that honestly. Reconcile the partial prompt record with complete exports from every AI tool used and compare requirements against original attachments. Version 1.0.0 was published to the public remote; subsequent unreleased enhancements may remain local, so check Git status and publish reviewed changes before portal submission. Verify the public remote, then submit its URL under the invitation's instructions before the deadline. See VERIFICATION.md for exact platform/testing limitations.

## 2026-10-30 — portal branding

User selected **ACI (Academic Integrity) Portal By Yotta**. A shared brand template now supplies the sidebar and login identity, with the expanded name in accessible labels/browser metadata/footer, and matching launcher/README display text. Existing technical paths remain stable. Django checks and the existing page-render test passed; desktop (1440×1000) and phone (375×812) branding were inspected. Refreshed the README desktop screenshot and added a phone branding screenshot; earlier workflow screenshots remain historical verification evidence.

## 2026-10-30 — first-run sign-in guidance

Added an in-page first-sign-in guide before the login fields: administrator username, where to copy its generated password, exact credentials-file/key instructions, and a non-destructive command to print credentials again. Expandable role descriptions explain all demo accounts; optional buttons fill usernames and clear a previous account’s password. They use normal Django authentication. Guidance and manual sign-in remain available without JavaScript.

Kept the guide discoverable on smaller screens with a compact brand introduction and no automatic input focus. Added matching input placeholders and Signing in progress text. Browser verification revealed an empty login view for an already-authenticated session; LoginView now redirects authenticated visitors to the workspace. Version 1.0.0 remains the unchanged baseline tag; this enhancement is listed under Unreleased.

## 2026-10-30 — reviewer workload and case-file navigation

User requested interactive summary cards, an Assigned to me default, newest-first reviewer queues, and clearer student/submission/timeline structure. Confirmed the proposed case-file order with the user.

Reviewer/instructor defaults now use current assignments across original and appeal phases, including completed cases. Assignment scope is independent of sorting; ended assignments are excluded. Sorting uses case opening date descending and ID descending for deterministic ties. Administrators/support retain all-case defaults; learners remain limited to their own work. Summary counts use the selected scope, with an explicit explanation above the cards.

Summary cards, tabs, filters and pagination progressively fetch authorized HTML and replace only the queue/summary. Cards clear search/page before applying a status and move smoothly to the queue; selection, focus, announcements, browser history and real fallback URLs keep navigation understandable. Superseded requests are aborted, reduced-motion preferences bypass smooth motion, and ordinary case-return links retain scope/search/sort/page and the queue anchor. No extra frontend runtime or API was added.

### Assignment scope navigation correction

The first status tab was labelled All cases while retaining the current assignment scope. A reviewer could therefore click it and still see only their own cases. Replaced the assignment dropdown with explicit Assigned to me / All cases links that apply immediately using the existing queue navigation. Renamed the status reset to All statuses. Scope switches preserve applied search, status and sort, and reset pagination; the form carries the selected scope in a hidden field. The reviewer default remains Assigned to me / Newest first. Links also work as normal GET navigation without JavaScript. Authorization and case data are unchanged.

Case files now present student ID/programme/email, the full escaped submission text and assessment metadata, evidence, learner response, retained decisions and full dated timeline. A section bar and case-actions link help on small screens; team/actions remain alongside on desktop. Domain write services and the v1.0.0 baseline tag are unchanged. Existing local reviewer data was preserved.
