from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urlpatterns import format_suffix_patterns
from danalysis import views


urlpatterns = [
    re_path("signup", views.signup),
    re_path("login", views.login),
    # re_path("test_token", views.test_token),
    path("admin/", admin.site.urls),
    path("device/", views.device_details_list),
    path("device/<str:id>", views.device_details),
    path("activeusers/lastyear", views.active_users_last_year_grouped_by_month),
    path("toproutes/lastyear", views.top_routes_last_year),
    path(
        "inlinequestionresponses/lastyear",
        views.monthly_inline_question_feedback_last_year,
    ),
    path("inlinequestionfeedbackcount/", views.inline_question_feedback_count),
    path("workercount/", views.active_worker_count),
    path("chapterquestionfeedbackcount/", views.chapter_question_feedback_count),
    path("uniqueagecounts/", views.unique_age_counts),
    path("monthfeedbackcount", views.monthly_question_feedback_counts_2023),
    path("topansweredinlinequestions", views.top_answered_questions),
    path("routedevices/", views.route_devices),
    path("workercreatedat", views.worker_device_created_at),
    path("workerroutecount/", views.worker_route_count),
    path("organisationworkercount/", views.organisation_worker_count),
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
