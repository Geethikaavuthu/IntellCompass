from django.urls import path
from . import views

app_name = "monitoring"

urlpatterns = [
    path("lesson/<int:lesson_pk>/", views.monitor_view, name="monitor"),
]
