from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urlpatterns import format_suffix_patterns
from danalysis import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("device/", views.device_details_list),
    path("device/<str:id>", views.device_details),
    path("activeusers/lastyear", views.active_users_last_year_grouped_by_month),
    path("toproutes/lastyear", views.top_routes_last_year),
    path(
        "inlinequestionresponses/lastyear",
        views.monthly_inline_question_feedback_last_year,
    ),
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
