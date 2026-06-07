from django.urls import path
from . import views

urlpatterns = [
    path("admin-stats/", views.admin_analytics_api, name="api-admin-stats"),
]
