from django.urls import path
from . import api_views

urlpatterns = [
    path("", api_views.course_list_api, name="api-courses"),
    path("<int:pk>/", api_views.course_detail_api, name="api-course-detail"),
]
