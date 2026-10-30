from django.contrib.auth import views as auth_views
from django.urls import path
from integrity import views

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", views.case_list, name="cases"),
    path("cases/<str:pk>/", views.case_detail, name="case-detail"),
    path("flags/", views.flags, name="flags"),
    path("submissions/", views.submissions, name="submissions"),
    path("submissions/new/", views.submission_new, name="submission-new"),
    path("submissions/<str:pk>/", views.submission_detail, name="submission-detail"),
    path("policy/", views.rules, name="rules"),
    path("validation/", views.validation, name="validation"),
    path("explore/", views.walkthrough, name="walkthrough"),
]
handler403 = views.denied
handler404 = views.not_found
