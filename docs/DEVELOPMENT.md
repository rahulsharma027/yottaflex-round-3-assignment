# Development log

## Version 1 baseline

The user requested preserving the current implementation as version 1 before further interface and workflow enhancements. `CHANGELOG.md` and the annotated `v1.0.0` Git tag identify this baseline. Subsequent improvements should preserve the tag and receive their own commits/version notes.

## Version 1.1 release

At the user's request, version `v1.1.0` collects the guided login, interactive role-specific queues, structured case files and subsequent assignment-scope fixes. Release notes were generated from the four conventional commits since `v1.0.0` and edited for clarity. The original baseline tag is preserved. No runtime dependency or database migration changed in this release.

## First prioritized audit fix: learner response reachability

The audit exposed cases whose learner had no login, while every decision required a learner response. The user selected a sourced external-response workflow to preserve the ten-account demo. Added a staff-only service/form for administrators/support, with server-side source, notice, account-link, state and stale-version checks. Full response/source snapshots remain in attributed events; the latest external response is shown with its recorder and timestamp in the case file. Existing direct learner ownership and decision prerequisites remain enforced. No learner credentials, migration or generated dataset were changed. AUDIT_FIXES.md tracks this resolved issue and the remaining findings separately.

## Second prioritized audit fix: evidence replacement authority

Reproduced the audit exploit with a failing regression before changing the service. Added a shared current-evidence replacement policy: learners need both ownership of the case and authorship of the item; staff retain existing correction permissions. EvidenceForm now requires the authenticated user, filters replacement choices through the shared policy and explains separate rebuttals. The service checks the same policy inside its versioned transaction. No historical rows or decision references are rewritten. Added five regression tests and updated the existing history test to use an authorized correction. F2 is handled as a separate commit after F1; later findings remain open.

## Third prioritized audit fix: generator information boundaries

Added failing regressions for future appeal text and assessment/scenario coupling, then introduced generator revision 2. Original submissions contain fictional academic passages; separate seeded shuffled scenario/assessment plans remove the audited metadata shortcuts while keeping walkthrough IDs stable. Source observations and later attribution evidence remain in dated records. Distribution summaries join truth only after records-only detection. Regenerated packaged exports/proof on Python 3.12 and 3.14. Legacy workspaces warn and preserve data/passwords, with a documented separate-workspace route. No schema migration was needed. F4's temporal validator gap remains open.

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

Rahul's personal code/documentation/audit review and interface feedback are recorded in [CANDIDATE_REVIEW.md](ai/CANDIDATE_REVIEW.md); personal execution of automated/export checks is not claimed. The recovered two-chat user-message record and export boundaries are in [AI_USE.md](ai/AI_USE.md). Keep subsequent prompts/review activities current and perform the final requirement comparison against the [recovered sources](source/README.md). Version 1.1.0 remains the release tag for the interface enhancements after the preserved 1.0.0 baseline; later fixes/documentation are subsequent commits. F4–F6 remain open/deferred. Verify public access and submit the repository URL under the invitation's instructions before the deadline. See VERIFICATION.md for exact checks and remaining platform/testing limitations.

## 2026-10-31 — transparent AI use and visible reasoning

At the user's request, focused on submission documentation while deferring further audit fixes. Recovered both project chats' candidate-input messages and original context attachments, recorded privacy/export boundaries, expanded AI reliance by area and attributed candidate review from the actual conversation/confirmation. Added REASONING.md to connect the problem, assumptions, alternatives, decisions, regression approach, measured results and limitations. Updated README navigation and the latest verification snapshot so historical statements do not obscure current evidence. No source code, accounts, live records, generated dataset or release tags were changed.

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

Assignment scope is now offered only to the instructor role used by original and appeal reviewers. Academic/platform administrators and support always use the authorized workspace scope; learners retain their ownership scope. For these actors, an explicit `assignee=mine` URL is normalized to the appropriate default rather than showing a misleading empty assignment queue. The existing template capability flag controls visibility, so no duplicated role checks or CSS changes are required.

## 2026-10-30 — navy and blue theme preference

User requested dark blue navigation with light central pages. Replaced the forest/lime brand tokens with navy `#152e52`, blue `#245cb0`, ice `#bedbff`, and a light canvas `#f5f7fb`. Shared tokens cover primary actions, hover, selected scope/cards, focus and supporting surfaces. Updated the login panel/guide, tables, form controls, submission papers, section markers and timeline accents to remove the old green cast. Status badges, warning/error feedback and success notices retain their semantic colors. Dark navigation uses an ice focus outline, while light surfaces use a blue outline.

Kept the existing plain CSS, type, layout, local assets and workflow behavior. No theme-switcher, extra dependency or account setting was needed. This is an unreleased enhancement after v1.1.0; published version tags remain unchanged. README screenshots now show the blue workspace/login; earlier images remain historical verification.

Case files now present student ID/programme/email, the full escaped submission text and assessment metadata, evidence, learner response, retained decisions and full dated timeline. A section bar and case-actions link help on small screens; team/actions remain alongside on desktop. Domain write services and the v1.0.0 baseline tag are unchanged. Existing local reviewer data was preserved.
