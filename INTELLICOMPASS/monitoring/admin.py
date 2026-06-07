from django.contrib import admin
from .models import EngagementSession

@admin.register(EngagementSession)
class EngagementSessionAdmin(admin.ModelAdmin):
    list_display = ["student", "lesson", "avg_attention_score", "dominant_emotion", "started_at"]
