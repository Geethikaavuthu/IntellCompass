from django.urls import path
from . import views

app_name = "courses"

urlpatterns = [
    path("", views.course_list, name="list"),
    path("<int:pk>/", views.course_detail, name="detail"),
    path("<int:pk>/enroll/", views.enroll, name="enroll"),
    path("<int:course_pk>/lesson/<int:lesson_pk>/", views.lesson_view, name="lesson"),
    path("<int:course_pk>/lesson/<int:lesson_pk>/complete/", views.mark_lesson_complete, name="complete-lesson"),
    path("create/", views.create_course, name="create"),
    path("<int:pk>/manage/", views.manage_course, name="manage"),
    path("<int:course_pk>/add-lesson/", views.add_lesson, name="add-lesson"),
]
