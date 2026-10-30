from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Assessment, EvidenceItem, Learner, Reviewer, Decision

class PortalLoginForm(AuthenticationForm):
    """Keep the first-run instructions visible before visitors focus a field."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.pop("autofocus", None)
        self.fields["username"].widget.attrs["placeholder"] = "e.g. academic-admin"
        self.fields["password"].widget.attrs["placeholder"] = "Your generated account password"

class NamedChoice(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.name} · {obj.id}" if hasattr(obj, "name") else f"{obj.title} · {obj.id}"

class VersionForm(forms.Form):
    version = forms.IntegerField(widget=forms.HiddenInput)

class ReasonForm(VersionForm):
    reason = forms.CharField(min_length=15, max_length=5000, label="Reason", widget=forms.Textarea(attrs={"rows": 4}))

class ExternalResponseForm(ReasonForm):
    source_reference = forms.CharField(min_length=5, max_length=240, label="Source reference",
        help_text="Identify the received correspondence, such as a signed statement or email reference. No email is sent or fetched.")
    field_order = ["version", "reason", "source_reference"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["reason"].label = "Learner's response"
        self.fields["reason"].help_text = "Transcribe the learner's received response. Your staff account remains the recorder in the timeline."

class AssignmentForm(ReasonForm):
    reviewer = NamedChoice(queryset=Reviewer.objects.filter(active=True, user__is_active=True))
    replace = forms.ChoiceField(required=False, label="Replace assignment (optional)")
    field_order = ["version", "reviewer", "replace", "reason"]
    def __init__(self, *args, case, **kwargs):
        super().__init__(*args, **kwargs)
        phase = "appeal" if case.state == "appeal" else "original"
        self.fields["replace"].choices = [("", "Add another reviewer")] + [
            (a.id, a.reviewer.name) for a in case.assignments.select_related("reviewer").filter(phase=phase, ended_at=None)]
        self.fields["reason"].help_text = "Explain the assignment. Conflicts and appeal independence are checked on the server."

class EvidenceForm(VersionForm):
    title = forms.CharField(max_length=160)
    excerpt = forms.CharField(max_length=10000, widget=forms.Textarea(attrs={"rows": 4}))
    source_reference = forms.CharField(max_length=240, help_text="Use an identifiable reference. Sources are displayed as text and never fetched.")
    supersedes = forms.ModelChoiceField(queryset=EvidenceItem.objects.none(), required=False, label="New version of (optional)")
    def __init__(self, *args, case, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["supersedes"].queryset = case.evidence.filter(evidenceitem__isnull=True)

class DecisionForm(VersionForm):
    outcome = forms.ChoiceField(choices=[("", "Select an outcome")] + Decision.OUTCOMES)
    evidence = forms.ModelMultipleChoiceField(queryset=EvidenceItem.objects.none(), widget=forms.CheckboxSelectMultiple,
        label="Evidence considered", help_text="Choose the current evidence versions you actually considered.")
    rationale = forms.CharField(min_length=15, max_length=10000, widget=forms.Textarea(attrs={"rows": 5}))
    def __init__(self, *args, case, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["evidence"].queryset = case.evidence.filter(evidenceitem__isnull=True)

class TriageForm(forms.Form):
    action = forms.ChoiceField(choices=[("open", "Open a formal case"), ("dismiss", "Dismiss this flag with a reason")])
    reason = forms.CharField(min_length=15, max_length=5000, widget=forms.Textarea(attrs={"rows": 4}))

class SubmissionForm(forms.Form):
    learner = NamedChoice(queryset=Learner.objects.all())
    assessment = NamedChoice(queryset=Assessment.objects.all())
    title = forms.CharField(max_length=160)
    content = forms.CharField(max_length=20000, widget=forms.Textarea(attrs={"rows": 6}), label="Submission text")
    raw_score = forms.IntegerField(min_value=0, max_value=100, initial=45, label="Simulated raw similarity (%)")
    quoted_score = forms.IntegerField(min_value=0, max_value=100, initial=10, label="Disjoint quoted overlap (percentage points)")
    template_score = forms.IntegerField(min_value=0, max_value=100, initial=5, label="Disjoint template overlap (percentage points)")
    token = forms.CharField(widget=forms.HiddenInput)
    def clean(self):
        result = super().clean()
        if all(k in result for k in ["raw_score", "quoted_score", "template_score"]) and result["quoted_score"] + result["template_score"] > result["raw_score"]:
            raise forms.ValidationError("Quoted and template overlap cannot exceed raw similarity. Use non-overlapping components.")
        return result
