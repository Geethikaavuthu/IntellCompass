from django.urls import path
from . import api_views

urlpatterns = [
    path("me/", api_views.current_user, name="api-current-user"),
]
