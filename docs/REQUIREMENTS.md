# Requirement traceability

Source: interpretation in PROJECT_BREAKDOWN.md and LLM_PROJECT_PROMPT.md. Original attachments are absent here; candidate reconciliation against them remains a final task.

| Requirement / accepted priority | Implementation | Evidence |
|---|---|---|
| Ten related entities and complete field dictionary | models.py, migrations, SCHEMA.md, ERD | System/migration checks; FK/unique validation |
| Submissions, synthetic reports and versioned thresholds | services, report screens, IntegrityRule snapshot | Score reconciliation and report tests |
| Warnings never automatically become guilt | Explicit triage and human decision services | High-score test creates no case/decision |
| Eligibility, conflicts, multiple reviewers | Assignment, ReviewerConflict, reassignment history | Conflict/permission/stale tests |
| Evidence provenance and retained versions | EvidenceItem.supersedes; DecisionEvidence; events | Late/cross-case/version tests |
| Human decisions and learner opportunity | Notice/response/evidence/rationale prerequisites | Missing-prerequisite rejection |
| Independent appeal and closure | Appeal and retained decisions | Full successful appeal test; independence/closure rejection |
| Atomic traceability and state changes | Transactional events/triage; versions/receipts | Rollback and duplicate/stale tests; lifecycle replay |
| Full 10,000 / 1,000 / 300 volumes | Full generator; packaged archive | verification.json counts |
| Required positive scenarios | Scenario facts; historical cases; demo guide | Coverage counts; full baseline |
| Four negative scenarios | Isolated fixtures and separate process truth | Four expected type detections; zero baseline errors |
| Required immutable IDs and joins | Generator/counters; FK models | Pattern, unique, FK and SQL checks |
| Fixed seed, starter/full, reproducibility | Shared generator and two-run script | Byte/file-hash equality; seed variation |
| Separate ground truth | External truth files; records-only detector | Feature-leakage test; post-detection evaluation |
| CSV/JSON/SQL, manifest and summary | data/full-dataset.zip; export command | SQL round-trip and recorded hashes |
| Meaningful metrics | validation.py, DATASET.md formulas | Recorded actual denominators/results |
| All five actor roles | Profile and service permissions | Ownership/access/assignment/CSRF tests |
| Friendly responsive UI | Custom local templates/CSS; mobile navigation | Actual browser inspection in VERIFICATION.md |
| Simple non-destructive clone/run | run.py + README | Clean-copy and repeat-run verification |
| All reviewer material within this repo | Source, docs, archive, evidence in Yotta | Clean-copy run without parent files |
| AI prompts and reliance disclosure | docs/ai | Partial record explicit; export reconciliation pending |
| Meaningful history and clean repository | Component commits; gitignore | Tracked-file/diff inspection |
| Public GitHub and portal submission | Existing remote in README | Publication/submission status in VERIFICATION.md |

Documented assumptions: INT means integrity case; one report/submission and one original/appeal finding/case; no real detector or runtime AI; scores/triage policy/permission matrix and learner-response prerequisites are implementation choices. Hosted demo/formal tests are optional under recorded FAQ; mandatory validation and repeatability are included.
