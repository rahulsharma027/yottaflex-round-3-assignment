"""All interactive writes pass through these transactional domain operations."""
import hashlib
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.db.models import F, Q
from django.utils import timezone
from .models import (
    Appeal, Assignment, Case, CaseEvent, Counter, Decision, DecisionEvidence,
    EvidenceItem, IntegrityRule, Reviewer, ReviewerConflict, SimilarityReport, Submission, TriageRecord, SubmissionReceipt,
)

ADMINS = {"academic_admin", "platform_admin"}
STAFF = ADMINS | {"instructor", "support"}

def role(user):
    return getattr(getattr(user, "profile", None), "role", "")

def require_role(user, allowed):
    if role(user) not in allowed:
        raise PermissionDenied("Your account does not have permission for this action.")

def can_view(user, case):
    return role(user) in STAFF or case.report.submission.learner.user_id == user.pk

def allocate(prefix, width=6, initial=0):
    counter, _ = Counter.objects.get_or_create(name=prefix, defaults={"value": initial})
    Counter.objects.filter(pk=prefix).update(value=F("value") + 1)
    counter.refresh_from_db()
    return f"{prefix}{counter.value:0{width}d}"

def lock_case(case_id, version):
    if not Case.objects.filter(pk=case_id, version=version).update(version=F("version") + 1):
        raise ValidationError("This case changed in another tab or this action was already submitted. Reload and try again.")
    return Case.objects.select_related("report__submission__learner").get(pk=case_id)

def event(case, user, action, detail, related_id="", occurred_at=None):
    return CaseEvent.objects.create(id=allocate("EVT-", initial=10000), case=case, actor=user.username,
                                   action=action, detail=detail, related_id=related_id,
                                   occurred_at=occurred_at or timezone.now())

def reason_required(reason):
    if len(reason.strip()) < 15:
        raise ValidationError("Please give a meaningful reason of at least 15 characters.")

def eligible(case, reviewer, phase):
    if not reviewer.active:
        raise ValidationError("This reviewer is inactive.")
    if not reviewer.user_id or not reviewer.user.is_active:
        raise ValidationError("This reviewer needs an active workspace account before assignment or decision.")
    if ReviewerConflict.objects.filter(reviewer=reviewer, learner=case.report.submission.learner).exists():
        raise ValidationError("Conflict of interest: choose another reviewer.")
    if phase == "appeal" and Assignment.objects.filter(case=case, reviewer=reviewer, phase="original").exists():
        raise ValidationError("An appeal reviewer must be independent of every original reviewer, including previous assignments.")

@transaction.atomic
def triage_report(user, report_id, action, reason):
    require_role(user, ADMINS | {"instructor"})
    reason_required(reason)
    if action not in {"open", "dismiss"}:
        raise ValidationError("Choose a valid triage action.")
    if not SimilarityReport.objects.filter(pk=report_id, flagged=True, triage="pending").update(
        triage="case" if action == "open" else "dismissed", triage_reason=reason
    ):
        raise ValidationError("This flag was already triaged. Reload the queue.")
    report = SimilarityReport.objects.get(pk=report_id)
    TriageRecord.objects.create(id=f"TRI-{report.id}", report=report, action=action, actor=user.username, reason=reason)
    if action == "dismiss":
        return None
    case = Case.objects.create(id=allocate("INT-2026-", initial=300), report=report)
    event(case, user, "case_opened", reason, report.id)
    return case

@transaction.atomic
def assign_reviewer(user, case_id, version, reviewer_id, reason, replace_id=""):
    require_role(user, ADMINS)
    reason_required(reason)
    case = lock_case(case_id, version)
    if case.state not in {"triage", "review", "appeal"}:
        raise ValidationError("Reviewer assignment is available during review or appeal only.")
    phase = "appeal" if case.state == "appeal" else "original"
    reviewer = Reviewer.objects.get(pk=reviewer_id)
    eligible(case, reviewer, phase)
    if Assignment.objects.filter(case=case, reviewer=reviewer, phase=phase, ended_at=None).exists():
        raise ValidationError("This reviewer is already assigned.")
    if replace_id:
        old = Assignment.objects.filter(pk=replace_id, case=case, phase=phase, ended_at=None).first()
        if not old:
            raise ValidationError("The assignment to replace is no longer active.")
        old.ended_at = timezone.now()
        old.save(update_fields=["ended_at"])
    assignment = Assignment.objects.create(id=allocate("ASG-", initial=1000), case=case,
                                            reviewer=reviewer, phase=phase, reason=reason)
    if case.state == "triage":
        case.state = "review"
        case.save(update_fields=["state"])
    event(case, user, "reviewer_assigned", f"{reviewer.name} · {phase}. {reason}", assignment.id)
    return case

@transaction.atomic
def notify_learner(user, case_id, version, reason):
    require_role(user, ADMINS | {"support"})
    reason_required(reason)
    case = lock_case(case_id, version)
    if case.state not in {"triage", "review"} or case.notification_at:
        raise ValidationError("Notice is already recorded or this case is past initial review.")
    case.notification_at = timezone.now()
    case.save(update_fields=["notification_at"])
    event(case, user, "learner_notified", "Local in-app notice recorded. " + reason)
    return case

@transaction.atomic
def respond(user, case_id, version, reason):
    reason_required(reason)
    case = lock_case(case_id, version)
    if role(user) != "learner" or case.report.submission.learner.user_id != user.pk:
        raise PermissionDenied("Only this case's learner can submit a response.")
    if case.state not in {"review", "triage", "appeal"} or not case.notification_at:
        raise ValidationError("A response needs an open review and a recorded notice.")
    case.learner_response = reason
    case.save(update_fields=["learner_response"])
    event(case, user, "learner_response", reason)
    return case

@transaction.atomic
def add_evidence(user, case_id, version, title, excerpt, source_reference, supersedes_id=""):
    case = lock_case(case_id, version)
    if not can_view(user, case) or role(user) not in STAFF | {"learner"}:
        raise PermissionDenied
    if case.state not in {"triage", "review", "appeal"}:
        raise ValidationError("Open an appeal before adding late evidence to a decided case. Earlier evidence is retained.")
    for value in [title, excerpt, source_reference]:
        if not value.strip():
            raise ValidationError("Title, excerpt and source reference are required.")
    previous = None
    if supersedes_id:
        previous = EvidenceItem.objects.filter(pk=supersedes_id, case=case).first()
        if not previous or EvidenceItem.objects.filter(supersedes=previous).exists():
            raise ValidationError("Choose a current evidence version from this case to supersede.")
    item = EvidenceItem.objects.create(id=allocate(f"EVD-{case.id}-", width=3, initial=case.evidence.count()),
        case=case, title=title, excerpt=excerpt, source_reference=source_reference, added_by=user.username, supersedes=previous)
    event(case, user, "evidence_added", f"{title}. Source: {source_reference}" +
          (f". New version of {previous.id}" if previous else ""), item.id, item.added_at)
    return case

@transaction.atomic
def record_decision(user, case_id, version, outcome, rationale, evidence_ids):
    require_role(user, ADMINS | {"instructor"})
    reason_required(rationale)
    case = lock_case(case_id, version)
    if case.state not in {"review", "appeal"}:
        raise ValidationError("A decision requires an active review or appeal.")
    if outcome not in dict(Decision.OUTCOMES):
        raise ValidationError("Choose a valid decision outcome.")
    phase = "appeal" if case.state == "appeal" else "original"
    reviewer = Reviewer.objects.filter(user=user).first()
    if not reviewer or not Assignment.objects.filter(case=case, reviewer=reviewer, phase=phase, ended_at=None).exists():
        raise PermissionDenied("Only an assigned reviewer can record this decision.")
    eligible(case, reviewer, phase)
    if not case.notification_at or not case.learner_response.strip():
        raise ValidationError("Record learner notice and obtain a learner response before deciding.")
    selected = list(EvidenceItem.objects.filter(pk__in=set(evidence_ids), case=case))
    if not selected or len(selected) != len(set(evidence_ids)):
        raise ValidationError("Select at least one evidence item belonging to this case.")
    if any(EvidenceItem.objects.filter(supersedes=item).exists() for item in selected):
        raise ValidationError("Use the latest evidence version for a new decision.")
    decision = Decision.objects.create(id=allocate("DEC-", initial=1000), case=case, reviewer=reviewer,
        phase=phase, outcome=outcome, rationale=rationale)
    DecisionEvidence.objects.bulk_create([DecisionEvidence(id=f"{decision.id}-{n:03}", decision=decision, evidence=item)
                                         for n, item in enumerate(selected, 1)])
    case.state = "decided"
    if phase == "appeal":
        appeal = case.appeal
        appeal.resolution = "overturned" if outcome != appeal.original_decision.outcome else "upheld"
        appeal.resolved_at = decision.decided_at
        appeal.save(update_fields=["resolution", "resolved_at"])
        case.state, case.closed_at = "closed", decision.decided_at
    case.save(update_fields=["state", "closed_at"])
    event(case, user, "decision_recorded", f"{decision.get_outcome_display()} · {phase}. {rationale}", decision.id)
    if phase == "appeal":
        event(case, user, "appeal_resolved", f"Independent appeal review: {case.appeal.resolution}.", case.appeal.id)
        event(case, user, "case_closed", "Closed after independent appeal decision.")
    return case

@transaction.atomic
def submit_appeal(user, case_id, version, reason):
    reason_required(reason)
    case = lock_case(case_id, version)
    own = role(user) == "learner" and case.report.submission.learner.user_id == user.pk
    if not own and role(user) not in ADMINS:
        raise PermissionDenied("Only the learner or an academic administrator can submit an appeal.")
    if case.state not in {"decided", "closed"} or Appeal.objects.filter(case=case).exists():
        raise ValidationError("An appeal needs an original decision and only one appeal is supported per case.")
    original = case.decisions.get(phase="original")
    appeal = Appeal.objects.create(id=f"APL-{case.id}-01", case=case, original_decision=original, reason=reason)
    case.state, case.closed_at = "appeal", None
    case.save(update_fields=["state", "closed_at"])
    event(case, user, "appeal_submitted", reason, appeal.id)
    return case

@transaction.atomic
def close_case(user, case_id, version, reason):
    require_role(user, ADMINS)
    reason_required(reason)
    case = lock_case(case_id, version)
    if case.state != "decided" or not case.decisions.filter(phase="original").exists():
        raise ValidationError("Only a case with a recorded decision can be closed. Pending appeals need independent review.")
    case.state, case.closed_at = "closed", timezone.now()
    case.save(update_fields=["state", "closed_at"])
    event(case, user, "case_closed", reason)
    return case

@transaction.atomic
def create_submission(user, learner, assessment, title, content, raw_score, quoted_score, template_score, request_key=None):
    if role(user) == "learner":
        if learner.user_id != user.pk:
            raise PermissionDenied
    else:
        require_role(user, ADMINS | {"instructor"})
    if not title.strip() or not content.strip():
        raise ValidationError("Title and submission text are required.")
    if not all(0 <= score <= 100 for score in [raw_score, quoted_score, template_score]) or quoted_score + template_score > raw_score:
        raise ValidationError("Scores must be 0–100 and disjoint quotation/template overlap cannot exceed raw similarity.")
    now = timezone.now()
    rule = IntegrityRule.objects.filter(effective_from__lte=now).filter(
        Q(effective_to=None) | Q(effective_to__gt=now)
    ).order_by("-version").first()
    if not rule:
        raise ValidationError("No effective integrity rule is configured.")
    receipt = None
    if request_key:
        key = hashlib.sha256(f"{user.pk}:{request_key}".encode()).hexdigest()
        receipt, _ = SubmissionReceipt.objects.get_or_create(pk=key, defaults={"user": user})
        if receipt.submission_id:
            return receipt.submission
    submission = Submission.objects.create(id=allocate("SUB-2026-", initial=10000), learner=learner,
        assessment=assessment, title=title, content=content)
    adjusted = raw_score - quoted_score - template_score
    flagged = adjusted >= rule.threshold
    SimilarityReport.objects.create(id=f"SIM-{submission.id}-01", submission=submission, rule=rule,
        raw_score=raw_score, quoted_score=quoted_score, template_score=template_score, adjusted_score=adjusted,
        flagged=flagged, threshold_snapshot=rule.threshold, generated_at=now,
        source_reference="synthetic://interactive/manual-simulation", triage="pending" if flagged else "unflagged")
    if receipt:
        receipt.submission = submission
        receipt.save(update_fields=["submission"])
    return submission
