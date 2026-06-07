from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
import json

@login_required
def recommendations_view(request):
    return render(request, "recommendations/recommendations.html")

@login_required
def get_recommendations_api(request):
    """Get AI-powered learning recommendations via Gemini."""
    try:
        try:
            import google.generativeai as genai
        except ImportError:
            return JsonResponse({"error": "AI recommendations not available. Install optional dependency 'google-generativeai' and set GEMINI_API_KEY."}, status=501)
        from courses.models import Enrollment
        from quizzes.models import QuizAttempt

        if not settings.GEMINI_API_KEY:
            return JsonResponse({"error": "Gemini API key not configured."}, status=501)

        enrollments = list(Enrollment.objects.filter(
            student=request.user
        ).values_list("course__title", flat=True))
        attempts = list(QuizAttempt.objects.filter(
            student=request.user
        ).order_by("-completed_at")[:5].values("quiz__title", "score"))

        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""Based on this student's learning data, suggest 5 personalized learning recommendations.
        Enrolled courses: {enrollments}
        Recent quiz scores: {json.dumps(attempts, default=str)}
        Return JSON array: [{{"title": "...", "description": "...", "type": "course/video/practice", "priority": "high/medium/low"}}]
        Return ONLY the JSON array, no markdown."""

        response = model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0]
        recs = json.loads(text)
        return JsonResponse({"recommendations": recs})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
