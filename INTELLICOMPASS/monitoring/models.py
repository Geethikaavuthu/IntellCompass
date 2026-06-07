from django.db import models
from django.conf import settings
from courses.models import Lesson

class EngagementSession(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="engagement_sessions")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="engagement_sessions")
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    avg_attention_score = models.FloatField(default=0.0)
    avg_emotion_score = models.FloatField(default=0.0)
    dominant_emotion = models.CharField(max_length=20, blank=True)
    emotion_data = models.JSONField(default=dict, blank=True)
    attention_data = models.JSONField(default=dict, blank=True)
    duration_seconds = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.student.username} - {self.lesson.title} ({self.avg_attention_score:.0f}%)"
