import json
import secrets
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from . import forms, services
from .models import Assignment, Case, IntegrityRule, SimilarityReport, Submission, SeedState

def scoped_cases(user):
    qs = Case.objects.select_related("report__submission__learner", "report__submission__assessment", "report__rule").prefetch_related(
        "assignments__reviewer", "decisions")
    if services.role(user) == "learner":
        return qs.filter(report__submission__learner__user=user)
    services.require_role(user, services.STAFF)
    return qs

def paginate(request, qs):
    return Paginator(qs, 15).get_page(request.GET.get("page"))

@login_required
def case_list(request):
    qs = scoped_cases(request.user)
    current_role = services.role(request.user)
    can_filter_assignments = current_role == "instructor"
    default_assignee = "mine" if current_role == "instructor" else "all"
    assignee = request.GET.get("assignee", default_assignee)
    if assignee not in {"mine", "all"} or not can_filter_assignments:
        assignee = default_assignee
    if assignee == "mine":
        # A subquery avoids duplicates and keeps reviewer/ended checks on one assignment.
        current_assignments = Assignment.objects.filter(reviewer__user=request.user, ended_at__isnull=True)
        qs = qs.filter(pk__in=current_assignments.values("case_id"))
    counts = {"all": qs.count(), "review": qs.filter(state__in=["triage", "review"]).count(),
              "appeal": qs.filter(state="appeal").count(), "closed": qs.filter(state="closed").count(),
              "decided": qs.filter(state="decided").count()}
    state = request.GET.get("state", "")
    if state not in {"active", *dict(Case.STATES)}:
        state = ""
    if state == "active":
        qs = qs.filter(state__in=["triage", "review"])
    elif state in dict(Case.STATES):
        qs = qs.filter(state=state)
    query = request.GET.get("q", "").strip()
    if query:
        qs = qs.filter(Q(id__icontains=query) | Q(report__submission__learner__name__icontains=query) |
                       Q(report__submission__assessment__title__icontains=query))
    order = request.GET.get("sort", "newest")
    orders = {"newest": ("-opened_at", "-id"), "oldest": ("opened_at", "id"),
              "similarity": ("-report__adjusted_score", "-opened_at", "-id")}
    if order not in orders:
        order = "newest"
    return render(request, "integrity/case_list.html", {"page": paginate(request, qs.order_by(*orders[order])),
        "counts": counts, "query": query, "state": state, "sort": order, "title": "Case workspace",
        "assignee": assignee, "default_assignee": default_assignee, "can_filter_assignments": can_filter_assignments,
        "sort_label": {"newest": "Newest first", "oldest": "Oldest first", "similarity": "Highest adjusted overlap"}[order]})

@login_required
def case_detail(request, pk):
    case = get_object_or_404(scoped_cases(request.user), pk=pk)
    actions = {"assign": forms.AssignmentForm, "evidence": forms.EvidenceForm, "decision": forms.DecisionForm,
               "notify": forms.ReasonForm, "response": forms.ReasonForm, "external_response": forms.ExternalResponseForm,
               "appeal": forms.ReasonForm, "close": forms.ReasonForm}
    bound_action = request.POST.get("action") if request.method == "POST" else None
    action_forms = {}
    for name, form_class in actions.items():
        kwargs = {"case": case} if name in {"assign", "evidence", "decision"} else {}
        action_forms[name] = form_class(request.POST if name == bound_action else None, initial={"version": case.version}, auto_id=f"id_{name}_%s", **kwargs)
    if request.method == "POST":
        if bound_action not in actions:
            return HttpResponse("Unknown action.", status=400)
        form = action_forms[bound_action]
        if form.is_valid():
            d = form.cleaned_data
            args = [request.user, case.id, d["version"]]
            try:
                if bound_action == "assign":
                    services.assign_reviewer(*args, d["reviewer"].id, d["reason"], d["replace"])
                elif bound_action == "evidence":
                    services.add_evidence(*args, d["title"], d["excerpt"], d["source_reference"], d["supersedes"].id if d["supersedes"] else "")
                elif bound_action == "decision":
                    services.record_decision(*args, d["outcome"], d["rationale"], [e.id for e in d["evidence"]])
                elif bound_action == "external_response":
                    services.record_external_response(*args, d["reason"], d["source_reference"])
                else:
                    {"notify": services.notify_learner, "response": services.respond, "appeal": services.submit_appeal,
                     "close": services.close_case}[bound_action](*args, d["reason"])
            except ValidationError as exc:
                form.add_error(None, exc)
            else:
                messages.success(request, "Saved. The case timeline has been updated.")
                return redirect(request.get_full_path())
    current_role = services.role(request.user)
    phase = "appeal" if case.state == "appeal" else "original"
    assigned = case.assignments.filter(reviewer__user=request.user, phase=phase, ended_at=None).exists()
    appeal = getattr(case, "appeal", None)
    back = request.GET.get("back", reverse("cases"))
    if not back.startswith("/") or not url_has_allowed_host_and_scheme(back, allowed_hosts={request.get_host()}):
        back = reverse("cases")
    response_event = case.events.filter(action__in=["learner_response", "learner_response_recorded"]).order_by("-occurred_at", "-id").first()
    return render(request, "integrity/case_detail.html", {"case": case, "title": case.id,
        "submission": case.report.submission, "learner": case.report.submission.learner,
        "assigned_to_me": case.assignments.filter(reviewer__user=request.user, ended_at__isnull=True).exists(),
        "forms": action_forms, "bound_action": bound_action, "back": back,
        "evidence": case.evidence.order_by("added_at", "id"),
        "timeline": case.events.order_by("occurred_at", "id"), "decisions": case.decisions.prefetch_related("evidence").select_related("reviewer").order_by("decided_at"),
        "assignments": case.assignments.select_related("reviewer"), "appeal": appeal,
        "review_open": case.state in {"triage", "review", "appeal"},
        "can_decide": assigned and case.state in {"review", "appeal"},
        "can_notify": current_role in services.ADMINS | {"support"} and not case.notification_at and case.state in {"triage", "review"},
        "can_respond": current_role == "learner" and case.notification_at and case.state in {"triage", "review", "appeal"},
        "response_event": response_event,
        "can_record_external_response": current_role in services.ADMINS | {"support"} and
            case.report.submission.learner.user_id is None and case.notification_at and case.state in {"triage", "review", "appeal"},
        "can_appeal": (current_role in services.ADMINS or current_role == "learner") and case.state in {"decided", "closed"} and not appeal})

@login_required
def flags(request):
    services.require_role(request.user, services.STAFF)
    qs = SimilarityReport.objects.filter(flagged=True).select_related("submission__learner", "submission__assessment")
    triage = request.GET.get("triage", "pending")
    if triage in {"pending", "dismissed", "case"}:
        qs = qs.filter(triage=triage)
    query = request.GET.get("q", "").strip()
    if query:
        qs = qs.filter(Q(submission__learner__name__icontains=query) | Q(submission_id__icontains=query))
    return render(request, "integrity/flags.html", {"page": paginate(request, qs.order_by("-adjusted_score", "id")),
        "triage": triage, "query": query, "title": "Flag triage"})

@login_required
def submissions(request):
    qs = Submission.objects.select_related("learner", "assessment", "report")
    if services.role(request.user) == "learner":
        qs = qs.filter(learner__user=request.user)
    else:
        services.require_role(request.user, services.STAFF)
    query = request.GET.get("q", "").strip()
    if query:
        qs = qs.filter(Q(id__icontains=query) | Q(title__icontains=query) | Q(learner__name__icontains=query))
    return render(request, "integrity/submissions.html", {"page": paginate(request, qs.order_by("-submitted_at", "id")), "query": query, "title": "Submissions"})

@login_required
def submission_detail(request, pk):
    submission = get_object_or_404(Submission.objects.select_related("learner", "assessment", "report__rule"), pk=pk)
    if services.role(request.user) == "learner":
        if submission.learner.user_id != request.user.pk:
            raise PermissionDenied
    else:
        services.require_role(request.user, services.STAFF)
    report = submission.report
    form = forms.TriageForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            case = services.triage_report(request.user, report.id, **form.cleaned_data)
        except ValidationError as exc:
            form.add_error(None, exc)
        else:
            messages.success(request, "Triage recorded with your reason.")
            return redirect("case-detail", pk=case.id) if case else redirect("submission-detail", pk=pk)
    return render(request, "integrity/submission_detail.html", {"submission": submission, "report": report,
        "form": form, "can_triage": services.role(request.user) in services.ADMINS | {"instructor"} and report.triage == "pending", "title": pk})

@login_required
def submission_new(request):
    services.require_role(request.user, services.ADMINS | {"instructor", "learner"})
    if "submission_token" not in request.session:
        request.session["submission_token"] = secrets.token_urlsafe(24)
    form = forms.SubmissionForm(request.POST or None, initial={"token": request.session["submission_token"]})
    if services.role(request.user) == "learner":
        form.fields["learner"].queryset = form.fields["learner"].queryset.filter(user=request.user)
    if request.method == "POST" and form.is_valid():
        if not secrets.compare_digest(form.cleaned_data["token"], request.session["submission_token"]):
            form.add_error(None, "This submission was already saved or the form has expired. Reload before creating another.")
        else:
            values = {k: v for k, v in form.cleaned_data.items() if k != "token"}
            try:
                submission = services.create_submission(request.user, **values, request_key=form.cleaned_data["token"])
            except ValidationError as exc:
                form.add_error(None, exc)
            else:
                request.session["submission_token"] = secrets.token_urlsafe(24)
                messages.success(request, "Submission and simulated report created. A flag is an invitation to review.")
                return redirect("submission-detail", pk=submission.id)
    return render(request, "integrity/form_page.html", {"form": form, "title": "Create submission", "button": "Create submission & report"})

@login_required
def rules(request):
    return render(request, "integrity/rules.html", {"rules": IntegrityRule.objects.order_by("-version"), "title": "Integrity policy"})

@login_required
def validation(request):
    services.require_role(request.user, services.ADMINS)
    report_path = settings.BASE_DIR / "data" / "verification.json"
    report = json.loads(report_path.read_text(encoding="utf-8")) if report_path.exists() else None
    return render(request, "integrity/validation.html", {"report": report, "title": "Dataset validation", "seed_state": SeedState.objects.first()})

@login_required
def walkthrough(request):
    services.require_role(request.user, services.STAFF)
    examples = [
        ("INT-2026-000001", "01", "Read the context", "Attributed quotations", "See source notes, a learner response, and a reasoned decision that clears legitimate quotation."),
        ("INT-2026-000002", "02", "Question the signal", "Shared template overlap", "Follow a high-similarity warning through a review of the assignment template."),
        ("INT-2026-000003", "03", "Review together", "Multiple reviewers", "Two reviewers share a case. Sign in as reviewer to record an evidence-backed decision."),
        ("INT-2026-000004", "04", "Preserve the history", "An independent appeal", "Compare the original finding with new attribution evidence and the independent appeal decision."),
    ]
    cases = set(Case.objects.filter(pk__in=[e[0] for e in examples]).values_list("pk", flat=True))
    return render(request, "integrity/walkthrough.html", {"examples": [e for e in examples if e[0] in cases], "title": "Explore the workspace"})

def denied(request, exception=None):
    return render(request, "integrity/error.html", {"title": "Access restricted", "detail": "Your account cannot perform this action or view this record. Sign in with an appropriate demo account."}, status=403)

def not_found(request, exception=None):
    return render(request, "integrity/error.html", {"title": "Record not found", "detail": "This record is unavailable. Return to the workspace to find an accessible case."}, status=404)
