# Schema and data dictionary

Generated from `integrity/models.py` by `python scripts/document_schema.py`. Check migrations into Git with model changes.

All core and supporting application fields are listed below. SQL export tables use the lowercase model name and `_id` foreign-key columns. CSV uses empty cells for nulls; JSON uses null. SQL represents booleans as 0/1. Live user links are omitted from deterministic exports and attached only during local account creation.

IDs are immutable text primary keys unless a table explicitly uses an automatic integer. Deletion of referenced records is protected. No delete or in-place evidence/decision edit route is exposed. Char fields use Unicode; datetime values are timezone-aware ISO 8601 (UTC in exports, Asia/Kolkata in the interface). Scores and thresholds use percentage points on 0–100; case version is a positive optimistic-lock counter. Dates and historical IDs are fixed by the generator, while new actions use the current clock.

`Required` refers to database nullability; a blank text field stores an empty string when allowed. Django form requirements may be stricter. Constraints, lifecycle, cardinalities, and cross-table checks are documented in ARCHITECTURE.md and DATASET.md. Django's auth/session tables use the framework's standard migrations; passwords are hashed by Django and excluded from every export.

## Profile

| Field | Type | Required | Unique | Values / validation / relationship |
|---|---|---|---|---|
| `id` | BigAutoField | Yes | Yes | Primary key; Blank allowed; MinValueValidator: -9223372036854775808; MaxValueValidator: 9223372036854775807 |
| `user_id` | OneToOneField | Yes | Yes | FK → User.id; protected delete; 1:1 |
| `role` | CharField | Yes | No | Max 24 characters; Allowed: `learner`, `instructor`, `academic_admin`, `support`, `platform_admin`; MaxLengthValidator: 24 |

## Learner

| Field | Type | Required | Unique | Values / validation / relationship |
|---|---|---|---|---|
| `id` | CharField | Yes | Yes | Primary key; Max 80 characters; MaxLengthValidator: 80 |
| `name` | CharField | Yes | No | Max 120 characters; MaxLengthValidator: 120 |
| `email` | CharField | Yes | Yes | Max 254 characters; MaxLengthValidator: 254; Valid email format; synthetic .invalid domain |
| `programme` | CharField | Yes | No | Max 120 characters; MaxLengthValidator: 120 |
| `user_id` | OneToOneField | No | Yes | FK → User.id; protected delete; 1:1; Blank allowed |

## Assessment

| Field | Type | Required | Unique | Values / validation / relationship |
|---|---|---|---|---|
| `id` | CharField | Yes | Yes | Primary key; Max 80 characters; MaxLengthValidator: 80 |
| `title` | CharField | Yes | No | Max 160 characters; MaxLengthValidator: 160 |
| `course` | CharField | Yes | No | Max 80 characters; MaxLengthValidator: 80 |
| `due_at` | DateTimeField | Yes | No |  |

## IntegrityRule

| Field | Type | Required | Unique | Values / validation / relationship |
|---|---|---|---|---|
| `id` | CharField | Yes | Yes | Primary key; Max 80 characters; MaxLengthValidator: 80 |
| `version` | PositiveIntegerField | Yes | Yes | MinValueValidator: 0; MaxValueValidator: 9223372036854775807 |
| `title` | CharField | Yes | No | Max 160 characters; MaxLengthValidator: 160 |
| `threshold` | PositiveSmallIntegerField | Yes | No | MinValueValidator: 0; MaxValueValidator: 100 |
| `case_threshold` | PositiveSmallIntegerField | Yes | No | MinValueValidator: 0; MaxValueValidator: 100 |
| `effective_from` | DateTimeField | Yes | No |  |
| `effective_to` | DateTimeField | No | No | Blank allowed |
| `description` | TextField | Yes | No |  |

Constraint `valid_rule_thresholds`: `<CheckConstraint: condition=(AND: ('threshold__lte', 100), ('case_threshold__lte', 100), ('case_threshold__gte', F(threshold))) name='valid_rule_thresholds'>`

## Submission

| Field | Type | Required | Unique | Values / validation / relationship |
|---|---|---|---|---|
| `id` | CharField | Yes | Yes | Primary key; Max 80 characters; MaxLengthValidator: 80 |
| `learner_id` | ForeignKey | Yes | No | FK → Learner.id; protected delete; N:1 |
| `assessment_id` | ForeignKey | Yes | No | FK → Assessment.id; protected delete; N:1 |
| `title` | CharField | Yes | No | Max 160 characters; MaxLengthValidator: 160 |
| `content` | TextField | Yes | No |  |
| `submitted_at` | DateTimeField | Yes | No | Default: now |

## SimilarityReport

| Field | Type | Required | Unique | Values / validation / relationship |
|---|---|---|---|---|
| `id` | CharField | Yes | Yes | Primary key; Max 80 characters; MaxLengthValidator: 80 |
| `submission_id` | OneToOneField | Yes | Yes | FK → Submission.id; protected delete; 1:1 |
| `rule_id` | ForeignKey | Yes | No | FK → IntegrityRule.id; protected delete; N:1 |
| `raw_score` | PositiveSmallIntegerField | Yes | No | MinValueValidator: 0; MaxValueValidator: 100 |
| `quoted_score` | PositiveSmallIntegerField | Yes | No | MinValueValidator: 0; MaxValueValidator: 100 |
| `template_score` | PositiveSmallIntegerField | Yes | No | MinValueValidator: 0; MaxValueValidator: 100 |
| `adjusted_score` | PositiveSmallIntegerField | Yes | No | MinValueValidator: 0; MaxValueValidator: 100 |
| `flagged` | BooleanField | Yes | No |  |
| `threshold_snapshot` | PositiveSmallIntegerField | Yes | No | MinValueValidator: 0; MaxValueValidator: 100 |
| `generated_at` | DateTimeField | Yes | No |  |
| `source_reference` | CharField | Yes | No | Max 240 characters; MaxLengthValidator: 240 |
| `triage` | CharField | Yes | No | Max 16 characters; Allowed: `pending`, `dismissed`, `case`, `unflagged`; MaxLengthValidator: 16 |
| `triage_reason` | TextField | Yes | No | Blank allowed |

Constraint `scores_reconcile`: `<CheckConstraint: condition=(AND: ('raw_score__lte', 100), ('adjusted_score__lte', 100), ('raw_score', <CombinedExpression: F(quoted_score) + F(template_score) + F(adjusted_score)>)) name='scores_reconcile'>`

## Reviewer

| Field | Type | Required | Unique | Values / validation / relationship |
|---|---|---|---|---|
| `id` | CharField | Yes | Yes | Primary key; Max 80 characters; MaxLengthValidator: 80 |
| `name` | CharField | Yes | No | Max 120 characters; MaxLengthValidator: 120 |
| `department` | CharField | Yes | No | Max 120 characters; MaxLengthValidator: 120 |
| `active` | BooleanField | Yes | No | Default: True |
| `user_id` | OneToOneField | No | Yes | FK → User.id; protected delete; 1:1; Blank allowed |

## ReviewerConflict

| Field | Type | Required | Unique | Values / validation / relationship |
|---|---|---|---|---|
| `id` | CharField | Yes | Yes | Primary key; Max 80 characters; MaxLengthValidator: 80 |
| `reviewer_id` | ForeignKey | Yes | No | FK → Reviewer.id; protected delete; N:1 |
| `learner_id` | ForeignKey | Yes | No | FK → Learner.id; protected delete; N:1 |
| `reason` | CharField | Yes | No | Max 240 characters; MaxLengthValidator: 240 |

Constraint `unique_conflict`: `<UniqueConstraint: fields=('reviewer', 'learner') name='unique_conflict'>`

## Case

| Field | Type | Required | Unique | Values / validation / relationship |
|---|---|---|---|---|
| `id` | CharField | Yes | Yes | Primary key; Max 80 characters; MaxLengthValidator: 80 |
| `report_id` | OneToOneField | Yes | Yes | FK → SimilarityReport.id; protected delete; 1:1 |
| `state` | CharField | Yes | No | Max 16 characters; Allowed: `triage`, `review`, `decided`, `appeal`, `closed`; Default: triage; MaxLengthValidator: 16 |
| `opened_at` | DateTimeField | Yes | No | Default: now |
| `closed_at` | DateTimeField | No | No | Blank allowed |
| `version` | PositiveIntegerField | Yes | No | Default: 1; MinValueValidator: 0; MaxValueValidator: 9223372036854775807 |
| `notification_at` | DateTimeField | No | No | Blank allowed |
| `learner_response` | TextField | Yes | No | Blank allowed |

## Assignment

| Field | Type | Required | Unique | Values / validation / relationship |
|---|---|---|---|---|
| `id` | CharField | Yes | Yes | Primary key; Max 80 characters; MaxLengthValidator: 80 |
| `case_id` | ForeignKey | Yes | No | FK → Case.id; protected delete; N:1 |
| `reviewer_id` | ForeignKey | Yes | No | FK → Reviewer.id; protected delete; N:1 |
| `phase` | CharField | Yes | No | Max 12 characters; Allowed: `original`, `appeal`; MaxLengthValidator: 12 |
| `assigned_at` | DateTimeField | Yes | No | Default: now |
| `ended_at` | DateTimeField | No | No | Blank allowed |
| `reason` | TextField | Yes | No |  |

## EvidenceItem

| Field | Type | Required | Unique | Values / validation / relationship |
|---|---|---|---|---|
| `id` | CharField | Yes | Yes | Primary key; Max 80 characters; MaxLengthValidator: 80 |
| `case_id` | ForeignKey | Yes | No | FK → Case.id; protected delete; N:1 |
| `title` | CharField | Yes | No | Max 160 characters; MaxLengthValidator: 160 |
| `excerpt` | TextField | Yes | No |  |
| `source_reference` | CharField | Yes | No | Max 240 characters; MaxLengthValidator: 240 |
| `added_at` | DateTimeField | Yes | No | Default: now |
| `added_by` | CharField | Yes | No | Max 120 characters; MaxLengthValidator: 120 |
| `supersedes_id` | OneToOneField | No | Yes | FK → EvidenceItem.id; protected delete; 1:1; Blank allowed |

## Decision

| Field | Type | Required | Unique | Values / validation / relationship |
|---|---|---|---|---|
| `id` | CharField | Yes | Yes | Primary key; Max 80 characters; MaxLengthValidator: 80 |
| `case_id` | ForeignKey | Yes | No | FK → Case.id; protected delete; N:1 |
| `reviewer_id` | ForeignKey | Yes | No | FK → Reviewer.id; protected delete; N:1 |
| `phase` | CharField | Yes | No | Max 12 characters; Allowed: `original`, `appeal`; MaxLengthValidator: 12 |
| `outcome` | CharField | Yes | No | Max 16 characters; Allowed: `cleared`, `misconduct`; MaxLengthValidator: 16 |
| `rationale` | TextField | Yes | No |  |
| `decided_at` | DateTimeField | Yes | No | Default: now |

Constraint `one_decision_per_phase`: `<UniqueConstraint: fields=('case', 'phase') name='one_decision_per_phase'>`

## DecisionEvidence

| Field | Type | Required | Unique | Values / validation / relationship |
|---|---|---|---|---|
| `id` | CharField | Yes | Yes | Primary key; Max 80 characters; MaxLengthValidator: 80 |
| `decision_id` | ForeignKey | Yes | No | FK → Decision.id; protected delete; N:1 |
| `evidence_id` | ForeignKey | Yes | No | FK → EvidenceItem.id; protected delete; N:1 |

Constraint `unique_evidence_considered`: `<UniqueConstraint: fields=('decision', 'evidence') name='unique_evidence_considered'>`

## Appeal

| Field | Type | Required | Unique | Values / validation / relationship |
|---|---|---|---|---|
| `id` | CharField | Yes | Yes | Primary key; Max 80 characters; MaxLengthValidator: 80 |
| `case_id` | OneToOneField | Yes | Yes | FK → Case.id; protected delete; 1:1 |
| `original_decision_id` | OneToOneField | Yes | Yes | FK → Decision.id; protected delete; 1:1 |
| `reason` | TextField | Yes | No |  |
| `submitted_at` | DateTimeField | Yes | No | Default: now |
| `resolved_at` | DateTimeField | No | No | Blank allowed |
| `resolution` | CharField | Yes | No | Max 16 characters; Allowed: `upheld`, `overturned`; Blank allowed; MaxLengthValidator: 16 |

## CaseEvent

| Field | Type | Required | Unique | Values / validation / relationship |
|---|---|---|---|---|
| `id` | CharField | Yes | Yes | Primary key; Max 80 characters; MaxLengthValidator: 80 |
| `case_id` | ForeignKey | Yes | No | FK → Case.id; protected delete; N:1 |
| `action` | CharField | Yes | No | Max 48 characters; MaxLengthValidator: 48 |
| `actor` | CharField | Yes | No | Max 120 characters; MaxLengthValidator: 120 |
| `occurred_at` | DateTimeField | Yes | No | Default: now |
| `detail` | TextField | Yes | No |  |
| `related_id` | CharField | Yes | No | Max 80 characters; Blank allowed; MaxLengthValidator: 80 |

## Counter

| Field | Type | Required | Unique | Values / validation / relationship |
|---|---|---|---|---|
| `name` | CharField | Yes | Yes | Primary key; Max 80 characters; MaxLengthValidator: 80 |
| `value` | PositiveIntegerField | Yes | No | Default: 0; MinValueValidator: 0; MaxValueValidator: 9223372036854775807 |

## SeedState

| Field | Type | Required | Unique | Values / validation / relationship |
|---|---|---|---|---|
| `key` | CharField | Yes | Yes | Primary key; Max 32 characters; MaxLengthValidator: 32 |
| `mode` | CharField | Yes | No | Max 16 characters; MaxLengthValidator: 16 |
| `seed` | PositiveIntegerField | Yes | No | MinValueValidator: 0; MaxValueValidator: 9223372036854775807 |
| `installed_at` | DateTimeField | Yes | No | Default: now |

## TriageRecord

| Field | Type | Required | Unique | Values / validation / relationship |
|---|---|---|---|---|
| `id` | CharField | Yes | Yes | Primary key; Max 80 characters; MaxLengthValidator: 80 |
| `report_id` | OneToOneField | Yes | Yes | FK → SimilarityReport.id; protected delete; 1:1 |
| `action` | CharField | Yes | No | Max 12 characters; Allowed: `open`, `dismiss`; MaxLengthValidator: 12 |
| `actor` | CharField | Yes | No | Max 120 characters; MaxLengthValidator: 120 |
| `reason` | TextField | Yes | No |  |
| `occurred_at` | DateTimeField | Yes | No | Default: now |

## SubmissionReceipt

| Field | Type | Required | Unique | Values / validation / relationship |
|---|---|---|---|---|
| `id` | CharField | Yes | Yes | Primary key; Max 64 characters; MaxLengthValidator: 64 |
| `user_id` | ForeignKey | Yes | No | FK → User.id; protected delete; N:1 |
| `submission_id` | OneToOneField | No | Yes | FK → Submission.id; protected delete; 1:1 |
