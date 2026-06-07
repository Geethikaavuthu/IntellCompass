from django.urls import path
from . import views

urlpatterns = [
    path("generate/", views.generate_quiz_api, name="api-generate-quiz"),
]
