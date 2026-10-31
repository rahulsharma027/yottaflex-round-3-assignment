# Problem, decisions and evidence

Current documentation snapshot: 2026-10-31 (Asia/Kolkata), after F1–F3. This is an explanation of the implemented solution and its evidence, not a claim that every requirement or open audit finding has been resolved.

## The problem and the intended boundary

The [supplied statement](source/PROJECT_STATEMENT.txt) asks for an end-to-end academic-integrity workflow and a reproducible synthetic dataset. A similarity warning must lead to human consideration rather than automatic guilt. The system therefore separates report flags, case lifecycle state and reasoned decision outcomes. A closed case can be cleared; an appeal can overturn a finding while retaining the original record.

The deliverables are a working local application, linked synthetic data with the required scenarios/exports, and evidence explaining and checking both. This is a process simulation, not a plagiarism-detection model. The original [submission guidance and FAQ](source/README.md), [requirement mapping](REQUIREMENTS.md), [schema](SCHEMA.md) and [dataset rules](DATASET.md) give the detail behind this explanation.

## Explicit assumptions

- One fictional institution and synthetic records; institution-wide staff read access is a demo permission policy. Learners see their own work.
- Similarity is simulated using disjoint percentage-point deductions: adjusted = raw − quoted − template. Threshold 20 and the historical case-opening band at 35 are implementation assumptions, not rules supplied by the assessor. Interactive case opening always requires human triage.
- Notice and a learner response precede decisions. Notice is recorded in-app; no email delivery or statutory waiting period is implied.
- Multiple original reviewers are supported, with one original finding and one independent appeal finding per case. Consensus voting and repeated appeal rounds are outside scope.
- The ten demo accounts provide role coverage rather than a login for every synthetic learner. Unlinked learners participate through sourced correspondence captured by administrators/support.
- `INT` identifies a case. Stable generated IDs, dates and references describe fictional history; development commits use their actual timestamps.

## Key choices and trade-offs

| Choice | Reason for choosing it | Cost or limitation accepted |
|---|---|---|
| Django templates, local assets and SQLite | One launcher and no required frontend build, cloud account or external database; framework auth/forms/migrations reduce setup work | SQLite serializes writes; production concurrency and institutional identity would need a different deployment design |
| Authorized services as the write boundary | Forms improve feedback, while services independently enforce consequential rules; case changes and audit events share an atomic transaction and version guard | More explicit checks; application-managed history remains editable by database administrators |
| Explicit human triage and evidence-backed decisions | A high score is a review signal, and legitimate quotation/template overlap must be represented | More workflow steps; these checks cannot establish the quality of a human's reasoning |
| Append-only evidence versions and retained decision references | Corrections should not change the evidence that supported an earlier finding | History is more complex; current-version choices and actor permissions must be checked together |
| Independent appeal reviewer | Every original participant, including reassigned reviewers, must be excluded from the appeal | A case can wait for an eligible reviewer; a second account alone is not proof of independence |
| Separate evaluation truth and record-only detection | Known expected outcomes should not be operational input features | Designed fixtures and shared modeling assumptions still limit what the evaluation proves |
| Progressive queue navigation over server HTML | Filters, browser history, smooth scrolling and fallback links work without a second API/frontend runtime | This does not replace a full accessibility audit; known mobile semantics/contrast gaps remain open |
| Non-destructive seed revisions | Reviewer-created records and passwords must survive upgrades | Existing users must choose a fresh workspace to see generator revision 2 |

These choices were proposed/implemented with heavy AI assistance. Candidate priorities and actual review are attributed in [AI_USE.md](ai/AI_USE.md) and [CANDIDATE_REVIEW.md](ai/CANDIDATE_REVIEW.md).

## How a consequential action is handled

For a decision, the view loads an authorized case and validates the form; the service checks role, current assignment, review phase, conflict/independence, notice, response, rationale and evidence. A case-version claim, state mutation, decision/evidence references and timeline event are committed together or rolled back. A stale browser tab cannot silently overwrite a newer action. See [services.py](../integrity/services.py) and the lifecycle/permission diagrams in [ARCHITECTURE.md](ARCHITECTURE.md).

F1 demonstrates why reachability matters: requiring a response without offering unlinked learners a legitimate response route created dead ends. The chosen repair records received correspondence with its source and real staff recorder, while preserving the decision prerequisite and ten-account demo.

F2 demonstrates why a hidden button is insufficient: the original service allowed a learner to supersede staff evidence. A shared actor-aware replacement policy now filters both form choices and service writes; learners add separate rebuttals or revise their own current evidence. Historical versions and earlier decision references remain.

F3 demonstrates why valid joins alone are insufficient: the initial synthetic text disclosed later appeal information and assessment/scenario assignments created a deterministic shortcut. Revision 2 uses academic original text, dated later evidence and separately shuffled plans. All five families now occur under each assessment; 1,342 of 2,000 learners have both truth outcomes. These safeguards address those shortcuts without proving universal statistical independence.

## Testing approach and the evidence it provides

Workflow tests exercise a complete review/independent appeal, then remove prerequisites or alter authorization to check rejection and rollback. F1–F3 include regressions reproducing the identified failures. Dataset tests check IDs, joins, arithmetic, dates, lifecycle, SQL round-trip, scenario coverage and reproducibility. Seed tests check fresh/current/legacy behavior and preservation. Browser checks inspect real forms, role navigation and selected desktop/phone/tablet surfaces; they supplement the automated suite.

| Latest recorded evidence | Observation | Practical limit |
|---|---|---|
| Application tests at F3 | 46 passed on Python 3.14.10 | Agent-executed tests, not candidate execution or exhaustive correctness proof |
| Full baseline exports | 10,000 submissions, 1,000 flags and 300 cases; zero baseline findings | Valid under the implemented rules, not every possible process failure |
| Four isolated invalid scenarios | 4 detected fixture/type pairs, 0 false positives/false negatives | Four controlled examples, not real-world detection accuracy |
| Repeatability and archive checks | Two-run file hashes match; exported hashes also match across tested Python 3.12/3.14 runs; ZIP entries checked against manifest | Only the recorded environments were tested; full normal-install bootstrap on every supported platform was not established |
| Interface/launcher checks | Selected responsive screens, setup, repeat launch, persistence, port handling and disposable reset tested | Full assistive-technology, platform and sustained-load coverage remains unverified |

Sources: [VERIFICATION.md](VERIFICATION.md), [verification.json](../data/verification.json), [Python 3.14 report](../data/python314-verification.json) and [tests](../integrity/tests/). The proof evaluates the packaged baseline, not later manual edits to the live database. Detection consumes records before evaluation joins expected labels, but the generator/validator/tests can still share blind spots. The audit found gaps despite a previously passing suite.

## Remaining limitations and reviewer checks

F4 (response-event chronology validation), F5 (mobile semantics/contrast) and F6 (complete disclosure/review reconciliation) remain open/deferred in [AUDIT_FIXES.md](AUDIT_FIXES.md). This documentation pass improves the available disclosure and reasoning; it does not close those findings. No production hosting, SSO/MFA, email delivery, attachment uploads, immutable database audit trail or real similarity detector is claimed.

To assess the explanation, use the [manual walkthrough](WALKTHROUGH.md) to compare prerequisites before/after a response, inspect evidence revision ownership and trace the retained original/appeal decisions. The optional verification command writes separate ignored proof output. [README.md](../README.md) explains setup and [candidate review](ai/CANDIDATE_REVIEW.md) distinguishes Rahul's actual reported work from agent-executed checks. No additional test-suite or browser execution is implied by this documentation-only update.
