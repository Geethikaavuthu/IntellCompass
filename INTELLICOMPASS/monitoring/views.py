from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
import json
from .models import EngagementSession

@login_required
def monitor_view(request, lesson_pk):
    """Page with webcam-based TensorFlow.js monitoring."""
    return render(request, "monitoring/monitor.html", {"lesson_pk": lesson_pk})

@login_required
def save_engagement(request):
    """API endpoint to save engagement data from TensorFlow.js."""
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)
    try:
        data = json.loads(request.body)
        session = EngagementSession.objects.create(
            student=request.user,
            lesson_id=data["lesson_id"],
            avg_attention_score=data.get("attention_score", 0),
            avg_emotion_score=data.get("emotion_score", 0),
            dominant_emotion=data.get("dominant_emotion", ""),
            emotion_data=data.get("emotion_data", {}),
            attention_data=data.get("attention_data", {}),
            duration_seconds=data.get("duration", 0),
            ended_at=timezone.now(),
        )
        return JsonResponse({"id": session.id, "status": "saved"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
