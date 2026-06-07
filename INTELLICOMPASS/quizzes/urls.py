from django.urls import path
from . import views

app_name = "quizzes"

urlpatterns = [
    path("course/<int:course_pk>/", views.quiz_list, name="list"),
    path("<int:pk>/take/", views.take_quiz, name="take"),
    path("result/<int:pk>/", views.quiz_result, name="result"),
]
