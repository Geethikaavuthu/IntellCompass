from django.urls import path
from . import views

app_name = "feedback"

urlpatterns = [
    path("course/<int:course_pk>/", views.submit_feedback, name="submit"),
]
