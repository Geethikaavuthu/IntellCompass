from django.db import models
from django.conf import settings
from courses.models import Course, Lesson

class Feedback(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="feedbacks")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="feedbacks", null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="feedbacks", null=True, blank=True)
    rating = models.PositiveIntegerField(choices=[(i,i) for i in range(1,6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        target = self.course.title if self.course else self.lesson.title if self.lesson else "General"
        return f"{self.student.username} → {target} ({self.rating}★)"
