from django.urls import path
from . import api_views

urlpatterns = [
    path("list/", api_views.feedback_list, name="api-feedback-list"),
]
