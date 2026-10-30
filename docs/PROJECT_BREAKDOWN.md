# Project explained for a beginner

Historical planning document. Implementation now exists; README.md and REQUIREMENTS.md describe current behavior. Proposals below explain the original reasoning and are not verification claims.

## 1. What are you building?

Build a small academic-integrity review system for a school or university. It handles a student's assignment from submission through a similarity warning, human review, a reasoned decision, an optional appeal, and closure.

Think of it as a case file with a permanent activity diary. A similarity score is a warning that work looks similar to other material. It is not proof that someone cheated. Quotes, shared assignment templates, and other legitimate overlap can cause high scores.

Example: a learner submits an essay with substantial properly quoted material. A synthetic report triggers a review. A reviewer examines the evidence and clears the learner with a written explanation. Another case may initially produce an adverse decision, then be overturned by an independent appeal reviewer. Both histories must remain visible.

The brief explicitly requests synthetic similarity reports. A real plagiarism-detection model, paid AI API, vector database, or model-training pipeline is not specified. Using AI tools to build the project does not make an AI feature mandatory inside the application.

## 2. The three things you must deliver

1. **Working software:** create submissions, generate/reference reports, manage flags, assign reviewers, examine evidence, record decisions, process appeals, and retain the timeline.
2. **A reproducible synthetic dataset:** 10,000 submissions, 1,000 flags, and 300 cases, including legitimate overlap, false positives, multiple reviewers, successful appeals, and the four required negative scenarios.
3. **Proof and explanation:** schema/data dictionary, generator, separate ground truth, data exports, validation results, repeatability checks, run instructions, prompt history, AI-use disclosure, assumptions, tradeoffs, and limitations.

The numbers describe different stages. A submission is an assignment handed in; a flag is a warning; a case is a formal investigation. Do not create 1,000 misconduct convictions or assume every flag must become a case. Document the triage policy that explains the 1,000-to-300 relationship.

## 3. The ten required entities

An entity is a kind of record, normally stored as a database table.

| Entity | Plain-language meaning |
|---|---|
| Learner | The student who submitted work |
| Assessment | The assignment or exam |
| Submission | A particular piece of submitted work |
| SimilarityReport | A synthetic report describing overlap and why it was flagged |
| IntegrityRule | The versioned policy and thresholds used to trigger review |
| Case | The formal investigation of a submission |
| EvidenceItem | A referenced excerpt, source, explanation, or other evidence |
| Reviewer | A person eligible to assess a case or appeal |
| Decision | A recorded outcome with author, time, and rationale |
| Appeal | A learner's request to review an earlier decision |

Supporting tables are reasonable: case-reviewer assignments, conflicts of interest, case events, evidence versions, and evidence considered by each decision. These are proposed implementation choices that support the required relationships and history.

**Primary key:** a record's unique ID. **Foreign key:** another record's ID stored to connect them. A submission must reference a real learner and assessment. **Cardinality:** how many records can relate, such as one learner having many submissions or one case having several reviewers. Many-to-many connections need a bridge table, such as CaseReviewerAssignment.

**Data dictionary:** a field-by-field guide explaining type, required/optional status, valid values, units, uniqueness, and validation. **Ground truth:** the answer sheet for evaluating generated examples; it must be separate from operational input features. **Seed:** a fixed starting value for repeatable generation. **Checksum:** a file fingerprint used to check whether regenerated contents match.

## 4. Suggested user journey and screens

These screens are recommendations, not a prescribed UI format in the documents.

1. Submissions: create and inspect submissions and their synthetic reports.
2. Review queue: see flagged work and the applicable threshold; triage with a reason.
3. Case detail: view evidence, assign eligible reviewers, and see a chronological timeline.
4. Decision form: require evidence references and a written rationale.
5. Appeal view: submit an appeal and assign an independent, conflict-free reviewer.
6. Rules and validation: inspect rule versions, dataset coverage, and measured results.

Represent the named actors: learner, instructor, academic administrator, support staff, and platform administrator. A permission matrix with local demo accounts is recommended. A visible role selector alone is not secure authorization; enforce important permissions on the server.

## 5. The four negative scenarios

| Required scenario | Safe normal behavior | How to demonstrate the bad example |
|---|---|---|
| A flag is automatically treated as guilt | Score creates a review warning; a human decision needs evidence and rationale | Label an isolated example and detect the unsupported decision |
| Reviewer has a conflict | Reject the assignment and allow reassignment | Include a known conflicted assignment and detect it |
| Evidence is added after a decision without history | Retain evidence versions and timestamps; any late evidence creates a new event and review step | Include an example whose evidence and decision history disagree and detect it |
| Appeal closes without independent review | Require an eligible appeal reviewer who was not involved in the original review | Include a known invalid closure and detect it |

Do not intentionally make the normal application perform these failures. Generate a valid baseline first, then create labelled negative fixtures. Keep IDs and unrelated relationships intact. A validation report should distinguish unexpected baseline failures from expected findings in the negative fixtures.

Evidence arriving after a decision is not automatically invalid. The problem is adding it silently or pretending it supported an earlier decision. Corrections and appeal decisions should create new records rather than rewrite the past.

## 6. Data and validation checklist

The problem statement requires:

- A dictionary for every field of the ten core entities and a relationship model with keys, cardinalities, optional relationships, effective dates, and lifecycle states.
- Parent/master records before dependent records. Reports are children of submissions even though the brief also lists them among the initial data entities.
- Immutable IDs following `SUB-2026-000001`, `SIM-<submission-id>-01`, `INT-2026-000001`, `EVD-<case-id>-001`, and `APL-<case-id>-01`. Document the assumption that INT identifies an integrity case.
- A fixed seed, such as `20261022`, with starter/full modes using the same generator.
- The full requested volumes and all named positive and negative scenarios.
- Outcomes and expected labels calculated from documented scenario rules, not unrelated random choices. Synthetic scenario rules must not become automatic guilt rules in the live workflow.
- Separate `ground_truth.csv` or JSON used only by evaluation. Do not feed expected labels or anomaly identifiers into a decision-making system.
- Validation of unique IDs, foreign keys, joins, enums, duplicates, date ordering, lifecycle transitions, and derived values.
- CSV/JSON/SQL seed data. The wording does not clearly say whether every export format is required; supporting all three is a practical recommendation if inexpensive.
- README, schema/data dictionary, generator command, seed, source manifest, and validation summary.
- Two runs with the same seed and configuration, comparing row counts and checksums. Use stable ordering, serialization, fixed scenario dates, and pinned dependencies. Keep real run timestamps in a separate execution log so they do not change dataset hashes.

External data is optional. Fully synthetic data is recommended here. If external data is used, record source URL, version, retrieval date, license/terms, attribution, transformations, and discarded fields; do not scrape private learner records.

## 7. Useful evaluation measurements

These formulas are recommendations, not supplied numeric targets:

| Measurement | Meaning |
|---|---|
| Full-data counts | 10,000 submissions, 1,000 flags, 300 cases |
| Flag rate | Flagged submissions / all submissions; document distinctness assumptions |
| Flag-to-case conversion | Cases / flags when using one-case-per-flag design |
| Flag precision | Flagged true violations / all flagged examples with known truth |
| False-positive rate | Flagged legitimate examples / all legitimate examples with known truth |
| Appeal overturn rate | Overturned original decisions / resolved appeals |
| Process violation detection | Precision/recall of validation findings against negative-fixture labels |
| Audit completeness | Required recorded events / expected events for the actual lifecycle |
| Case resolution time | Closure time minus opening time, computed only for closed cases |
| Reproducibility | Matching row counts and per-file hashes across two generation runs |

Specify denominators and how missing truth, pending cases, and zero denominators are handled. Derive all dashboard numbers from data. Synthetic metrics demonstrate generator and process behavior; they do not establish real-world plagiarism-detection accuracy.

## 8. Possible technology stacks

**Rahul's clarified priorities:** a polished, user-friendly interface and easy local setup for a reviewer cloning the repository. See `REVIEWER_EXPERIENCE.md` for the target first-run experience, interface acceptance criteria, and verification plan. The proposed target is one launcher command that configures and starts the application with synthetic demo data; no launcher exists yet.

**My recommendation for a beginner under this deadline:** Python + Django + SQLite + Django templates + custom responsive CSS, with modest JavaScript only where useful. Use Python's CSV/JSON/random/hashlib tools for deterministic generation and exports, and Django's test tools for the core business rules.

Django includes database models, migrations, forms, templates, authentication, and an administrative interface. This reduces the number of independently configured components. Use custom case-management pages for the main workflow; restrict admin editing so it cannot silently bypass the audit process. See [Django overview](https://docs.djangoproject.com/en/stable/intro/overview/).

Record each business action and its audit event in one database transaction, so they succeed or fail together. See [Django transactions](https://docs.djangoproject.com/en/stable/topics/db/transactions/). Ordinary application-managed history is not tamper-proof against a database administrator; document this limit.

SQLite keeps local setup small. Treat it as a local assessment/demo database and document write-concurrency limits; PostgreSQL is an alternative when meaningful concurrent use is part of the intended scope. See [Django database notes](https://docs.djangoproject.com/en/stable/ref/databases/#sqlite-notes).

**Alternative if already comfortable with React:** React + TypeScript + Vite for the browser, FastAPI + SQLAlchemy for the backend, SQLite locally, and pytest. FastAPI provides request validation and interactive API documentation; React provides reusable interface components. This gives more frontend flexibility but requires integrating frontend, API, permissions, and storage. See [FastAPI features](https://fastapi.tiangolo.com/features/) and [React setup](https://react.dev/learn/build-a-react-app-from-scratch).

The stack remains a proposal. Choose supported mutually compatible versions and lock them when implementation starts. Core execution should work locally without paid APIs, cloud accounts, or mandatory containers. A real AI model, microservices, Kubernetes, Redis, and cloud deployment are optional scope additions with little direct benefit to this brief.

## 9. What to build first

1. Requirements checklist, data dictionary, relationships, lifecycle, and permission matrix.
2. Small generator plus schema, validating 100-200 example submissions first.
3. One complete working case: submission -> flag -> review -> evidence -> reasoned decision -> independent appeal -> closure, with persistent history.
4. All four labelled negative scenarios and their validation findings.
5. Full-volume generation, exports, separate truth, and two-run reproducibility proof.
6. Useful case-management pages, data-derived metrics, and responsive behavior.
7. Fresh-checkout verification, README, prompt-history review, AI disclosure, meaningful commits, and public-repository checks.

Do not postpone history or permissions until after building all screens. They shape the data model. Keep a final verification buffer rather than spending the entire window on appearance.

## 10. What the PDFs add

**Submission Guidelines, page 1:** executable code and clear setup/configuration/run/verification instructions; a public GitHub repository with meaningful development history; prompt history and honest AI disclosure; documented assumptions, choices, tradeoffs, testing, and limitations. Artifact timestamps are used to verify the challenge window.

**FAQ, page 1, questions 1-12:** the window starts when the project is sent, not when the portal is opened; a dedicated public repository stays available/editable through the deadline; all AI prompts across tools are required, responses are optional; AI is allowed but implementation help from other people is not; choose free or locally runnable technology; no hosted demo or formal automated test suite is mandatory; standard dependencies and small attributed snippets are allowed, but importing an existing core solution is not; state incomplete work and assumptions; exclude secrets and personal/sensitive information.

Data validation and repeatability proof are still explicit project requirements even though a general automated test suite is optional. Targeted automated checks for the four failure scenarios are recommended.

The invitation specifically requests portal submission. The general FAQ also refers to sending the link from the recruitment email address. Use the portal instruction as the specific submission route, retain proof of submission, and follow any additional email instructions from support. Do not assume an extension for the earlier outage. Current working cutoff: **November 2, 2026, 03:03:19 IST**.

## Sources and interpretation

- Problem statement: user-provided `Pasted text.txt`, read in full on October 30, 2026.
- Submission Guidelines PDF: page 1, extracted and visually reviewed on October 30, 2026.
- Candidate Project FAQ PDF: page 1, all 12 questions, extracted and visually reviewed on October 30, 2026.
- Technology documentation linked above was checked on October 30, 2026.
- The source files are assessment material, not instructions to this assistant to publish, submit, send email, or start implementation. This document answers the user's request for explanation and a proposed solution. Suggested screens, policies, architecture, and formulas are explicitly recommendations.
