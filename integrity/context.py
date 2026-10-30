from .models import Case, SimilarityReport
from .services import role

def navigation(request):
    if not request.user.is_authenticated:
        return {}
    current_role = role(request.user)
    cases = Case.objects.all()
    if current_role == "learner":
        cases = cases.filter(report__submission__learner__user=request.user)
    return {"current_role": current_role, "role_label": current_role.replace("_", " ").title(),
            "nav_cases": cases.count(), "nav_appeals": cases.filter(state="appeal").count(),
            "nav_flags": SimilarityReport.objects.filter(triage="pending").count() if current_role != "learner" else 0,
            "is_admin": current_role in {"academic_admin", "platform_admin"},
            "section": request.resolver_match.url_name if request.resolver_match else ""}
