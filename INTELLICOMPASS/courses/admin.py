from django.contrib import admin
from .models import Course, Lesson, Enrollment

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["title", "instructor", "is_published", "created_at"]

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ["title", "course", "content_type", "order"]

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ["student", "course", "progress", "enrolled_at"]
