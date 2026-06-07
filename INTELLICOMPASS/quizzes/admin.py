from django.contrib import admin
from .models import Quiz, Question, QuizAttempt

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ["title", "course", "is_adaptive", "created_at"]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["text", "quiz", "difficulty", "correct_answer"]

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ["student", "quiz", "score", "completed_at"]
