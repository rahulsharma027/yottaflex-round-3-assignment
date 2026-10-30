"""Operational records. Evaluation labels deliberately live outside this schema."""
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Q
from django.utils import timezone

PROTECT = models.PROTECT
SCORE = [MinValueValidator(0), MaxValueValidator(100)]

class Record(models.Model):
    id = models.CharField(primary_key=True, max_length=80)
    class Meta:
        abstract = True
        ordering = ["id"]
    def __str__(self):
        return self.id

class Profile(models.Model):
    ROLES = [(x, x.replace("_", " ").title()) for x in
             ["learner", "instructor", "academic_admin", "support", "platform_admin"]]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=PROTECT)
    role = models.CharField(max_length=24, choices=ROLES)

class Learner(Record):
    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    programme = models.CharField(max_length=120)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=PROTECT)

class Assessment(Record):
    title = models.CharField(max_length=160)
    course = models.CharField(max_length=80)
    due_at = models.DateTimeField()

class IntegrityRule(Record):
    version = models.PositiveIntegerField(unique=True)
    title = models.CharField(max_length=160)
    threshold = models.PositiveSmallIntegerField(validators=SCORE)
    case_threshold = models.PositiveSmallIntegerField(validators=SCORE)
    effective_from = models.DateTimeField()
    effective_to = models.DateTimeField(null=True, blank=True)
    description = models.TextField()
    class Meta(Record.Meta):
        constraints = [models.CheckConstraint(condition=Q(threshold__lte=100) & Q(case_threshold__lte=100)
                      & Q(case_threshold__gte=models.F("threshold")), name="valid_rule_thresholds")]

class Submission(Record):
    learner = models.ForeignKey(Learner, on_delete=PROTECT, related_name="submissions")
    assessment = models.ForeignKey(Assessment, on_delete=PROTECT, related_name="submissions")
    title = models.CharField(max_length=160)
    content = models.TextField()
    submitted_at = models.DateTimeField(default=timezone.now)

class SimilarityReport(Record):
    TRIAGE = [(x, x.title()) for x in ["pending", "dismissed", "case", "unflagged"]]
    submission = models.OneToOneField(Submission, on_delete=PROTECT, related_name="report")
    rule = models.ForeignKey(IntegrityRule, on_delete=PROTECT)
    raw_score = models.PositiveSmallIntegerField(validators=SCORE)
    quoted_score = models.PositiveSmallIntegerField(validators=SCORE)
    template_score = models.PositiveSmallIntegerField(validators=SCORE)
    adjusted_score = models.PositiveSmallIntegerField(validators=SCORE)
    flagged = models.BooleanField(db_index=True)
    threshold_snapshot = models.PositiveSmallIntegerField(validators=SCORE)
    generated_at = models.DateTimeField()
    source_reference = models.CharField(max_length=240)
    triage = models.CharField(max_length=16, choices=TRIAGE, db_index=True)
    triage_reason = models.TextField(blank=True)
    class Meta(Record.Meta):
        constraints = [models.CheckConstraint(
            condition=Q(raw_score__lte=100) & Q(adjusted_score__lte=100)
            & Q(raw_score=models.F("quoted_score") + models.F("template_score") + models.F("adjusted_score")),
            name="scores_reconcile")]

class Reviewer(Record):
    name = models.CharField(max_length=120)
    department = models.CharField(max_length=120)
    active = models.BooleanField(default=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=PROTECT)
    @property
    def initials(self):
        return "".join(word[0] for word in self.name.replace("Dr. ", "").replace("Prof. ", "").split()[:2])

class ReviewerConflict(Record):
    reviewer = models.ForeignKey(Reviewer, on_delete=PROTECT)
    learner = models.ForeignKey(Learner, on_delete=PROTECT)
    reason = models.CharField(max_length=240)
    class Meta(Record.Meta):
        constraints = [models.UniqueConstraint(fields=["reviewer", "learner"], name="unique_conflict")]

class Case(Record):
    STATES = [(x, x.replace("_", " ").title()) for x in ["triage", "review", "decided", "appeal", "closed"]]
    report = models.OneToOneField(SimilarityReport, on_delete=PROTECT, related_name="case")
    state = models.CharField(max_length=16, choices=STATES, default="triage", db_index=True)
    opened_at = models.DateTimeField(default=timezone.now)
    closed_at = models.DateTimeField(null=True, blank=True)
    version = models.PositiveIntegerField(default=1)
    notification_at = models.DateTimeField(null=True, blank=True)
    learner_response = models.TextField(blank=True)

class Assignment(Record):
    PHASES = [("original", "Original review"), ("appeal", "Appeal review")]
    case = models.ForeignKey(Case, on_delete=PROTECT, related_name="assignments")
    reviewer = models.ForeignKey(Reviewer, on_delete=PROTECT)
    phase = models.CharField(max_length=12, choices=PHASES)
    assigned_at = models.DateTimeField(default=timezone.now)
    ended_at = models.DateTimeField(null=True, blank=True)
    reason = models.TextField()

class EvidenceItem(Record):
    case = models.ForeignKey(Case, on_delete=PROTECT, related_name="evidence")
    title = models.CharField(max_length=160)
    excerpt = models.TextField()
    source_reference = models.CharField(max_length=240)
    added_at = models.DateTimeField(default=timezone.now)
    added_by = models.CharField(max_length=120)
    supersedes = models.OneToOneField("self", null=True, blank=True, on_delete=PROTECT)
    def __str__(self):
        return f"{self.title} · {self.id}"

class Decision(Record):
    OUTCOMES = [("cleared", "No misconduct found"), ("misconduct", "Misconduct substantiated")]
    case = models.ForeignKey(Case, on_delete=PROTECT, related_name="decisions")
    reviewer = models.ForeignKey(Reviewer, on_delete=PROTECT)
    phase = models.CharField(max_length=12, choices=Assignment.PHASES)
    outcome = models.CharField(max_length=16, choices=OUTCOMES)
    rationale = models.TextField()
    decided_at = models.DateTimeField(default=timezone.now)
    evidence = models.ManyToManyField(EvidenceItem, through="DecisionEvidence")
    class Meta(Record.Meta):
        constraints = [models.UniqueConstraint(fields=["case", "phase"], name="one_decision_per_phase")]

class DecisionEvidence(Record):
    decision = models.ForeignKey(Decision, on_delete=PROTECT, related_name="evidence_links")
    evidence = models.ForeignKey(EvidenceItem, on_delete=PROTECT)
    class Meta(Record.Meta):
        constraints = [models.UniqueConstraint(fields=["decision", "evidence"], name="unique_evidence_considered")]

class Appeal(Record):
    case = models.OneToOneField(Case, on_delete=PROTECT, related_name="appeal")
    original_decision = models.OneToOneField(Decision, on_delete=PROTECT)
    reason = models.TextField()
    submitted_at = models.DateTimeField(default=timezone.now)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolution = models.CharField(max_length=16, blank=True, choices=[("upheld", "Upheld"), ("overturned", "Overturned")])

class CaseEvent(Record):
    case = models.ForeignKey(Case, on_delete=PROTECT, related_name="events")
    action = models.CharField(max_length=48)
    actor = models.CharField(max_length=120)
    occurred_at = models.DateTimeField(default=timezone.now)
    detail = models.TextField()
    related_id = models.CharField(max_length=80, blank=True)
    @property
    def action_label(self):
        return self.action.replace("_", " ").capitalize()
    class Meta(Record.Meta):
        ordering = ["occurred_at", "id"]

class Counter(models.Model):
    """Updated within a transaction to allocate immutable, collision-free IDs."""
    name = models.CharField(primary_key=True, max_length=80)
    value = models.PositiveIntegerField(default=0)

class SeedState(models.Model):
    key = models.CharField(primary_key=True, max_length=32)
    mode = models.CharField(max_length=16)
    seed = models.PositiveIntegerField()
    installed_at = models.DateTimeField(default=timezone.now)

class TriageRecord(Record):
    report = models.OneToOneField(SimilarityReport, on_delete=PROTECT, related_name="triage_record")
    action = models.CharField(max_length=12, choices=[("open", "Open case"), ("dismiss", "Dismiss flag")])
    actor = models.CharField(max_length=120)
    reason = models.TextField()
    occurred_at = models.DateTimeField(default=timezone.now)

class SubmissionReceipt(models.Model):
    id = models.CharField(primary_key=True, max_length=64)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=PROTECT)
    submission = models.OneToOneField(Submission, null=True, on_delete=PROTECT)
