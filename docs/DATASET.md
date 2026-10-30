# Synthetic dataset and evaluation

Generator: `integrity/dataset.py`; seed **20261022**. Full mode has **10,000 submissions / 1,000 flags / 300 cases**; starter has **100 / 10 / 3**. Each submission has one report. Full data includes 2,000 learners, five assessments, six reviewers, one rule version, conflicts, triage/assignment/evidence/decision/appeal/event records. Exact totals are in the manifest.

## Rules and scenarios

Flag means adjusted overlap at or above its threshold snapshot. In integer percentage points, `adjusted = raw − quoted − template`. Quotation and template components are disjoint, so deductions cannot double-count. This is a transparent simulation, not a span detector.

First 300 full-mode reports have adjusted scores 35–65, next 700 have 20–34, remaining 9,000 have 0–19. Threshold 20 creates 1,000 distinct flags. Historical human triage opens cases at ≥35 with a reason, yielding 300 cases. Remaining flags split into 350 pending and 350 recorded dismissals. These are synthetic assumptions, not assessor-supplied misconduct rules. Live case creation always requires human triage.

Five equally distributed scenario families cycle by submission number. Facts are assigned first; outcomes derive from them rather than independent random labels:

| Scenario | Source fact | Resolved historical outcome |
|---|---|---|
| Legitimate quotation | Attributed passage and matching bibliography | Cleared |
| Shared template | Matching content supplied with the assessment | Cleared |
| False positive/common language | Independent work shares technical vocabulary | Cleared; multiple original reviewers |
| Omitted attribution | Initial bundle misses dated bibliography; supplied on appeal | Original finding overturned independently |
| Unattributed copying | No quote, attribution, or draft supports copied passage | Misconduct after evidence-led review |

Randomness varies score components inside scenario ranges. Pending cases retain expected evaluation outcomes but have no fabricated live finding. The successful-appeal truth label names a scenario family; actual appeal records exist only for formal cases. Full data includes all required paths; starter's three cases omit the appeal walkthrough, but its four isolated negative fixtures use slices from the same full generator. Dates are fixed synthetic September 2026 history, not backdated development artifacts. New interactive actions use the current clock.

Interactive submission/case counters start above the full reserved baseline ranges, even in starter mode, to avoid collisions; gaps are intentional. Evidence counters are per-case. Supporting entities use stable table-prefixed IDs where the statement does not prescribe a pattern.

## Negative fixtures and truth

Generate a valid baseline, deep-copy complete relational case slices, then preserve these deliberate mutations in `negative_fixtures.json`. Foreign keys remain valid. They are never imported into the live app.

| Fixture | Mutation and detection |
|---|---|
| automatic_guilt | Misconduct without rationale/evidence links; detect unsupported finding as proxy for flag-as-guilt |
| conflicted_reviewer | Known supervisor assigned and authors finding; join assignment to learner conflict |
| unlogged_late_evidence | Earlier decision's evidence moved after decision with provenance event removed; detect timing/history mismatch |
| nonindependent_appeal | Original reviewer assigned to and authors appeal; detect original participation |

`validate(records)` consumes operational records only. `evaluate()` joins detections to separate `negative_ground_truth.json` afterward. `ground_truth.json` contains intended misconduct, scenario rule, expected final outcome and linked IDs. Labels and anomaly names are absent from operational models/features. The unsupported-finding detector does not establish how a real human reached a decision; it detects missing process support.

## Package and commands

`data/full-dataset.zip` keeps repeated text compact in Git. Contents:

- `data.json`: operational tables sorted by ID; `<table>.csv`: per-table UTF-8/LF exports.
- `seed.sql`: standalone SQLite evaluation schema and inserts, not Django migrations/auth. Import into an empty database; `PRAGMA foreign_key_check` validates its joins.
- `ground_truth.json`: separate intended misconduct labels and documented scenario rules.
- `negative_fixtures.json` / `negative_ground_truth.json`: isolated bad records / separate expected process labels.
- `manifest.json`: generator version, seed, mode, counts, synthetic source and per-file SHA-256.

CSV empty cells mean nullable/blank values according to SCHEMA.md; JSON uses null, SQL uses NULL and booleans 0/1. User links/passwords are excluded and attached separately during local setup.

`python run.py` calls `seed_demo`: dependency-ordered, transactional import from the same generator, excluding truth and invalid fixtures. Seed completion is marked only on success. Later runs preserve data; unmarked existing submissions cause a refusal. Export commands never edit the live database.

No external data, scraping, real learners, external source passages or dataset licensing obligations are involved. Institution, names, passages and academic findings are fictional. `synthetic://` references are identifiers, not URLs to fetch. Standard dependencies retain their own licenses; core work was newly authored with disclosed AI assistance.

## Validation and metrics

Checks cover volumes; ID uniqueness/patterns; foreign keys/joins; one-to-one constraints; enums; timezone/date ordering; rule intervals/snapshots; score arithmetic; flag/triage consistency; triage actor/reason/time; case origin/closure; assignments/conflicts; decision phase/author/rationale/evidence; notice/response; evidence provenance/availability/version order; appeal origin/independence/resolution; and event-replayed lifecycle. The validator assumes the documented table/object structure rather than accepting arbitrary untrusted JSON. Corruption tests and a SQL round-trip check exercise its boundaries.

All ratios use 0–1, rounded to six decimals. Zero denominator means null/unavailable. Flag metrics include only reports with known separate truth; all generated reports have truth. Pending appeals are excluded from resolved denominators; open cases from duration averages.

| Metric | Formula |
|---|---|
| Flag rate | Flagged known reports / known reports |
| Flag-to-case rate | Cases / flagged reports |
| Flag precision | Flagged true misconduct / flagged known reports |
| False-positive rate | Flagged legitimate reports / **all legitimate reports** |
| Appeal overturn rate | Overturned / resolved appeals |
| Closed-case mean hours | Sum(closed_at − opened_at in hours) / closed cases |
| Process detection precision | Correct distinct fixture/type detections / predicted pairs |
| Process detection recall | Correct distinct fixture/type detections / expected pairs |
| Audit-complete case rate | Cases without required-event, evidence-history or lifecycle findings / cases |

Multiple findings of one type in one fixture count once. Synthetic metrics characterize this generator and designed exceptions, not real-world plagiarism accuracy. The operational dashboard counts stored live records. The administrator evaluation view explicitly describes packaged-baseline results, not interactive edits.

## Two-run proof

`python scripts/verify_dataset.py --package` writes separate run-a/run-b directories, checks baseline and negative fixtures, compares counts and every exported checksum, then packages run-a. IDs, ordering, keys, UTF-8/LF serialization, dates and ZIP metadata are stable. `data/verification.json` records actual execution time, Python version, elapsed seconds, findings and hashes separately from hashed dataset content. Dependencies are pinned. Cross-version reproducibility is not claimed beyond environments actually tested.
