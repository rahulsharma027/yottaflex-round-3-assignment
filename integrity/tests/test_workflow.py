from datetime import timedelta
from html.parser import HTMLParser
from django.apps import apps
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied, ValidationError
from django.test import TestCase, Client, override_settings
from django.utils.html import escape
from integrity import services
from integrity.dataset import generate, TABLES
from integrity.models import (
    Assessment, Assignment, Case, CaseEvent, Decision, EvidenceItem, Learner, Profile, Reviewer, SimilarityReport, Submission, TriageRecord,
)

@override_settings(PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"])
class WorkflowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        data, _ = generate("starter")
        for table in TABLES:
            model = apps.get_model("integrity", table)
            fields = {field.attname: field for field in model._meta.concrete_fields}
            model.objects.bulk_create([model(**{k: fields[k].to_python(v) for k,v in row.items()}) for row in data[table]])
        for name, role in [("admin", "academic_admin"), ("platform_admin", "platform_admin"), ("reviewer", "instructor"), ("appeal", "instructor"),
                           ("conflicted", "instructor"), ("learner", "learner"), ("support", "support")]:
            user = User.objects.create_user(name, password="test-only-password")
            Profile.objects.create(user=user, role=role)
            setattr(cls, name, user)
        for name, rid in [("reviewer", "REV-001"), ("appeal", "REV-003"), ("conflicted", "REV-006")]:
            Reviewer.objects.filter(pk=rid).update(user=getattr(cls, name))
        Learner.objects.filter(pk="LRN-00001").update(user=cls.learner)

    def new_case(self):
        sub = services.create_submission(self.learner, Learner.objects.get(pk="LRN-00001"), Assessment.objects.first(),
            "New synthetic essay", "An entirely synthetic submission for a workflow test.", 75, 10, 5)
        case = services.triage_report(self.admin, sub.report.id, "open", "Source context needs formal evidence review.")
        return case

    def prepare_review(self):
        case = self.new_case()
        case = services.assign_reviewer(self.admin, case.id, case.version, "REV-001", "Independent original reviewer selected.")
        case = services.notify_learner(self.support, case.id, case.version, "Please review this in-app notice and respond.")
        case = services.respond(self.learner, case.id, case.version, "Please consider my dated bibliography and working draft.")
        case = services.add_evidence(self.support, case.id, case.version, "Source excerpt", "The synthetic source passage and draft comparison.", "synthetic://test/source")
        return case

    def test_complete_review_and_successful_independent_appeal(self):
        case = self.prepare_review()
        original_evidence = case.evidence.first()
        case = services.record_decision(self.reviewer, case.id, case.version, "misconduct", "The initial source comparison substantiates unattributed copying.", [original_evidence.id])
        original = case.decisions.get(phase="original")
        case = services.submit_appeal(self.learner, case.id, case.version, "A dated attribution page was missing from the original bundle.")
        case = services.assign_reviewer(self.admin, case.id, case.version, "REV-003", "Independent reviewer has no original involvement.")
        case = services.add_evidence(self.learner, case.id, case.version, "Attribution page", "The dated bibliography correctly attributes this passage.", "synthetic://test/bibliography")
        case = services.record_decision(self.appeal, case.id, case.version, "cleared", "The newly supplied attribution page explains the overlap and clears the learner.", list(case.evidence.values_list("id", flat=True)))
        self.assertEqual(case.state, "closed")
        self.assertEqual(case.appeal.resolution, "overturned")
        self.assertEqual(case.decisions.count(), 2)
        original.refresh_from_db()
        self.assertEqual(original.outcome, "misconduct")
        self.assertEqual(original.evidence.count(), 1)
        self.assertTrue(case.events.filter(action="appeal_resolved").exists())

    def test_flag_does_not_create_guilt_or_case_automatically(self):
        before = Case.objects.count()
        sub = services.create_submission(self.learner, Learner.objects.get(pk="LRN-00001"), Assessment.objects.first(),
            "Synthetic high similarity", "Synthetic source text with high overlap.", 90, 0, 0)
        self.assertTrue(sub.report.flagged)
        self.assertEqual(Case.objects.count(), before)
        self.assertFalse(Decision.objects.filter(case__report=sub.report).exists())

    def test_conflicted_assignment_rolls_back_state_and_audit(self):
        case = self.new_case()
        events = case.events.count()
        with self.assertRaisesMessage(ValidationError, "Conflict of interest"):
            services.assign_reviewer(self.admin, case.id, case.version, "REV-006", "Attempt assignment of a conflicted supervisor.")
        case.refresh_from_db()
        self.assertEqual(case.state, "triage")
        self.assertEqual(case.version, 1)
        self.assertEqual(case.events.count(), events)
        self.assertFalse(case.assignments.exists())

    def test_original_reviewer_cannot_review_appeal_even_after_reassignment(self):
        case = Case.objects.get(pk="INT-2026-000001")
        case = services.submit_appeal(self.learner, case.id, case.version, "Please reconsider the evidence independently.")
        with self.assertRaisesMessage(ValidationError, "independent"):
            services.assign_reviewer(self.admin, case.id, case.version, "REV-001", "Attempt reuse of the original case reviewer.")

    def test_decision_requires_evidence_rationale_notice_and_response(self):
        case = self.new_case()
        case = services.assign_reviewer(self.admin, case.id, case.version, "REV-001", "Eligible reviewer selected for original review.")
        with self.assertRaises(ValidationError):
            services.record_decision(self.reviewer, case.id, case.version, "misconduct", "A reasoned decision requires learner participation.", [])
        self.assertFalse(case.decisions.exists())
        case = self.prepare_review()
        with self.assertRaises(ValidationError):
            services.record_decision(self.reviewer, case.id, case.version, "misconduct", "A substantive explanation with no evidence is insufficient.", [])
        with self.assertRaises(ValidationError):
            services.record_decision(self.reviewer, case.id, case.version, "misconduct", "", list(case.evidence.values_list("id", flat=True)))

    def test_cross_case_evidence_is_rejected(self):
        case = self.prepare_review()
        other = EvidenceItem.objects.filter(case_id="INT-2026-000001").first()
        with self.assertRaisesMessage(ValidationError, "belonging to this case"):
            services.record_decision(self.reviewer, case.id, case.version, "cleared", "A valid explanation cannot use unrelated evidence.", [other.id])

    def test_late_evidence_requires_appeal_and_old_versions_are_preserved(self):
        case = Case.objects.get(pk="INT-2026-000001")
        with self.assertRaisesMessage(ValidationError, "Open an appeal"):
            services.add_evidence(self.admin, case.id, case.version, "Late material", "A new source.", "synthetic://late")
        case = services.submit_appeal(self.learner, case.id, case.version, "A new source requires an independent reconsideration.")
        previous = case.evidence.first()
        case = services.add_evidence(self.learner, case.id, case.version, "Corrected excerpt", "Corrected synthetic source reference.", "synthetic://corrected", previous.id)
        self.assertEqual(case.evidence.count(), 2)
        self.assertTrue(case.evidence.filter(supersedes=previous).exists())
        self.assertEqual(case.decisions.get(phase="original").evidence.first().id, previous.id)

    def test_pending_appeal_cannot_be_closed(self):
        case = Case.objects.get(pk="INT-2026-000001")
        case = services.submit_appeal(self.learner, case.id, case.version, "Please request independent appeal review.")
        with self.assertRaises(ValidationError):
            services.close_case(self.admin, case.id, case.version, "Attempt premature closure without appeal review.")

    def test_stale_action_and_duplicate_decision_are_rejected(self):
        case = self.prepare_review()
        version = case.version
        case = services.record_decision(self.reviewer, case.id, version, "cleared", "Evidence and attribution explain the source overlap.", list(case.evidence.values_list("id", flat=True)))
        with self.assertRaisesMessage(ValidationError, "already submitted"):
            services.record_decision(self.reviewer, case.id, version, "cleared", "Duplicate request with exactly the same evidence.", list(case.evidence.values_list("id", flat=True)))
        self.assertEqual(case.decisions.count(), 1)

    def test_permissions_are_enforced_in_services(self):
        case = self.prepare_review()
        with self.assertRaises(PermissionDenied):
            services.record_decision(self.admin, case.id, case.version, "cleared", "Admin is not this case's assigned reviewer.", list(case.evidence.values_list("id", flat=True)))
        with self.assertRaises(PermissionDenied):
            services.assign_reviewer(self.support, case.id, case.version, "REV-003", "Support must not be permitted to assign reviewers.")
        with self.assertRaises(PermissionDenied):
            services.respond(self.learner, "INT-2026-000003", 1, "Attempt to respond for a different learner's case.")

    def test_triage_is_recorded_with_actor_and_cannot_repeat(self):
        report = SimilarityReport.objects.filter(triage="pending").first()
        services.triage_report(self.admin, report.id, "dismiss", "Common language explains the remaining overlap.")
        self.assertEqual(TriageRecord.objects.get(report=report).actor, "admin")
        with self.assertRaises(ValidationError):
            services.triage_report(self.admin, report.id, "open", "A repeated request must not open another case.")

    def test_all_pages_render_and_search_pagination_preserve_context(self):
        self.client.force_login(self.admin)
        for url in ["/", "/?q=Aarav", "/?state=closed&sort=similarity&page=2", "/flags/", "/submissions/", "/submissions/new/",
                    "/submissions/SUB-2026-000001/", "/cases/INT-2026-000003/", "/policy/", "/validation/", "/explore/"]:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)
        response = self.client.get("/?q=unfindable")
        self.assertContains(response, "No cases match")

    def test_learner_cannot_read_others_or_evaluation(self):
        self.client.force_login(self.learner)
        self.assertEqual(self.client.get("/cases/INT-2026-000001/").status_code, 200)
        self.assertEqual(self.client.get("/cases/INT-2026-000003/").status_code, 404)
        for url in ["/validation/", "/flags/", "/submissions/SUB-2026-000003/", "/explore/"]:
            self.assertEqual(self.client.get(url).status_code, 403)

    def test_auth_csrf_and_unknown_record(self):
        self.assertEqual(self.client.get("/").status_code, 302)
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.admin)
        self.assertEqual(csrf_client.post("/cases/INT-2026-000003/", {"action": "close", "version": 1}).status_code, 403)
        self.client.force_login(self.admin)
        self.assertEqual(self.client.get("/cases/INT-2026-999999/").status_code, 404)
        self.assertEqual(self.client.get("/logout/").status_code, 405)

    def test_invalid_form_preserves_input_and_untrusted_text_is_escaped(self):
        self.client.force_login(self.admin)
        response = self.client.post("/cases/INT-2026-000003/", {"action": "assign", "version": 1,
            "reviewer": "REV-006", "reason": "Please assign the reviewer to this specific case.", "replace": "bad-id"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please assign the reviewer")
        EvidenceItem.objects.filter(case_id="INT-2026-000003").update(excerpt="<script>alert('untrusted')</script>")
        response = self.client.get("/cases/INT-2026-000003/")
        self.assertContains(response, "&lt;script&gt;")
        self.assertNotContains(response, "<script>alert")

    def test_submission_form_duplicate_token_and_score_validation(self):
        self.client.force_login(self.learner)
        self.client.get("/submissions/new/")
        token = self.client.session["submission_token"]
        payload = {"learner": "LRN-00001", "assessment": "ASM-001", "title": "Synthetic interactive form",
            "content": "A synthetic piece of academic writing for a local test.", "raw_score": 55, "quoted_score": 5, "template_score": 5, "token": token}
        self.assertEqual(self.client.post("/submissions/new/", payload).status_code, 302)
        response = self.client.post("/submissions/new/", payload)
        self.assertContains(response, "already saved")
        payload.update(token=self.client.session["submission_token"], quoted_score=99)
        self.assertContains(self.client.post("/submissions/new/", payload), "cannot exceed raw similarity")

    def test_external_return_url_is_not_trusted(self):
        self.client.force_login(self.admin)
        response = self.client.get("/cases/INT-2026-000003/?back=https://example.invalid")
        self.assertEqual(response.context["back"], "/")

    def test_submission_receipt_is_idempotent(self):
        values = [self.learner, Learner.objects.get(pk="LRN-00001"), Assessment.objects.first(),
                  "Repeated synthetic work", "A synthetic submission for duplicate-request testing.", 50, 5, 5]
        first = services.create_submission(*values, request_key="same-request")
        second = services.create_submission(*values, request_key="same-request")
        self.assertEqual(first.id, second.id)

    def test_inactive_workspace_account_cannot_receive_assignment(self):
        case = self.new_case()
        User.objects.filter(pk=self.appeal.pk).update(is_active=False)
        with self.assertRaisesMessage(ValidationError, "active workspace account"):
            services.assign_reviewer(self.admin, case.id, case.version, "REV-003", "Inactive account must not receive an actionable assignment.")

    def test_reassigned_original_reviewer_remains_ineligible_for_appeal(self):
        case = self.prepare_review()
        old = case.assignments.get(reviewer_id="REV-001")
        case = services.assign_reviewer(self.admin, case.id, case.version, "REV-003", "Replace original reviewer while preserving participation history.", old.id)
        case = services.record_decision(self.appeal, case.id, case.version, "cleared", "The evidence and response explain the overlapping material.", list(case.evidence.values_list("id", flat=True)))
        case = services.submit_appeal(self.learner, case.id, case.version, "Request independent reconsideration of the original review.")
        with self.assertRaisesMessage(ValidationError, "including previous assignments"):
            services.assign_reviewer(self.admin, case.id, case.version, "REV-001", "Attempt reuse of an ended original assignment.")

    def test_reviewer_queue_defaults_to_current_assignments_newest_first(self):
        first = Case.objects.get(pk="INT-2026-000001")
        Case.objects.filter(pk="INT-2026-000003").update(opened_at=first.opened_at + timedelta(hours=1))
        second = Case.objects.get(pk="INT-2026-000002")
        Assignment.objects.filter(case=second, reviewer_id="REV-001").update(ended_at=second.closed_at)
        unassigned = self.new_case()
        self.client.force_login(self.reviewer)
        response = self.client.get("/")
        ids = [case.id for case in response.context["page"]]
        self.assertEqual(response.context["assignee"], "mine")
        self.assertEqual(response.context["sort"], "newest")
        self.assertContains(response, 'aria-label="Case assignment scope"')
        self.assertEqual(ids, ["INT-2026-000003", "INT-2026-000001"])
        self.assertNotIn(unassigned.id, ids)
        self.assertEqual(response.context["counts"]["all"], 2)
        all_cases = self.client.get("/?assignee=all")
        self.assertEqual(all_cases.context["page"][0].id, unassigned.id)
        self.assertEqual(all_cases.context["counts"]["all"], 4)

    def test_assignment_filter_combines_with_status_search_and_sort(self):
        second = Case.objects.get(pk="INT-2026-000002")
        Assignment.objects.filter(case=second, reviewer_id="REV-001").update(ended_at=second.closed_at)
        self.client.force_login(self.reviewer)
        params = {"assignee": "mine", "state": "closed", "q": second.id, "sort": "oldest"}
        self.assertEqual(self.client.get("/", params).context["page"].paginator.count, 0)
        params["assignee"] = "all"
        response = self.client.get("/", params)
        self.assertEqual([case.id for case in response.context["page"]], [second.id])
        fallback = self.client.get("/?assignee=unknown&sort=unknown")
        self.assertEqual((fallback.context["assignee"], fallback.context["sort"]), ("mine", "newest"))

    def test_assignment_scope_links_switch_both_directions_and_keep_filters(self):
        class ScopeLinks(HTMLParser):
            def __init__(self, response):
                super().__init__()
                self.links = {}
                self.feed(response.content.decode())

            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if tag == "a" and "data-assignment-scope" in attrs:
                    self.links[attrs["data-assignment-scope"]] = attrs

        unassigned = self.new_case()
        self.client.force_login(self.reviewer)
        mine = self.client.get("/")
        links = ScopeLinks(mine).links
        self.assertEqual(links["mine"].get("aria-current"), "true")
        all_cases = self.client.get(links["all"]["href"])
        self.assertEqual(all_cases.context["assignee"], "all")
        self.assertIn(unassigned, all_cases.context["page"])
        links = ScopeLinks(all_cases).links
        self.assertEqual(links["all"].get("aria-current"), "true")
        mine_again = self.client.get(links["mine"]["href"])
        self.assertEqual(mine_again.context["assignee"], "mine")
        self.assertNotIn(unassigned, mine_again.context["page"])
        filtered = self.client.get("/?assignee=mine&state=closed&q=INT-2026&sort=oldest&page=2")
        switched = self.client.get(ScopeLinks(filtered).links["all"]["href"])
        self.assertEqual(switched.context["assignee"], "all")
        self.assertEqual(switched.context["state"], "closed")
        self.assertEqual(switched.context["query"], "INT-2026")
        self.assertEqual(switched.context["sort"], "oldest")
        self.assertEqual(switched.context["page"].number, 1)
        self.assertContains(switched, "All statuses")

    def test_assignment_scope_preserves_actor_access_boundaries(self):
        for actor in [self.admin, self.platform_admin, self.support]:
            self.client.force_login(actor)
            for params in [{}, {"assignee": "mine"}]:
                with self.subTest(actor=actor.username, params=params):
                    response = self.client.get("/", params)
                    self.assertEqual(response.context["assignee"], "all")
                    self.assertEqual(response.context["counts"]["all"], 3)
                    self.assertNotContains(response, 'aria-label="Case assignment scope"')
                    self.assertNotContains(response, "Assigned to me")
        self.client.force_login(self.learner)
        for assignee in ["all", "mine"]:
            response = self.client.get("/", {"assignee": assignee})
            self.assertEqual([case.id for case in response.context["page"]], ["INT-2026-000001"])
            self.assertNotContains(response, 'aria-label="Case assignment scope"')
            self.assertNotContains(response, "Assigned to me")
        self.assertEqual(self.client.get("/cases/INT-2026-000002/").status_code, 404)

    def test_case_file_includes_own_student_details_and_escaped_original_work(self):
        submission = Submission.objects.get(pk="SUB-2026-000001")
        submission.content = "Original submitted text. <script>alert('unsafe')</script>"
        submission.save(update_fields=["content"])
        self.client.force_login(self.learner)
        response = self.client.get("/cases/INT-2026-000001/")
        self.assertContains(response, submission.learner.id)
        self.assertContains(response, submission.learner.programme)
        self.assertContains(response, submission.learner.email)
        self.assertContains(response, escape(submission.title))
        self.assertContains(response, "Original submitted text.")
        self.assertContains(response, "&lt;script&gt;")
        self.assertNotContains(response, "<script>alert('unsafe')</script>")
        self.assertNotContains(response, "learner2@example.invalid")
