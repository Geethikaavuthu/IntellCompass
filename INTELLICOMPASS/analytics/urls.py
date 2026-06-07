from django.urls import path
from . import views

app_name = "analytics"

urlpatterns = [
    path("student/", views.student_analytics, name="student"),
]
