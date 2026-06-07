from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from accounts.models import User
from courses.models import Course, Enrollment
from quizzes.models import QuizAttempt
from monitoring.models import EngagementSession
from feedback.models import Feedback

@login_required
def student_analytics(request):
    attempts = QuizAttempt.objects.filter(student=request.user).order_by("-completed_at")
    enrollments = Enrollment.objects.filter(student=request.user)
    sessions = EngagementSession.objects.filter(student=request.user).order_by("-started_at")[:20]
    return render(request, "analytics/student_analytics.html", {
        "attempts": attempts, "enrollments": enrollments, "sessions": sessions,
    })

@login_required
def admin_analytics_api(request):
    if not request.user.is_admin_user():
        return JsonResponse({"error": "Forbidden"}, status=403)
    return JsonResponse({
        "students": User.objects.filter(role="student").count(),
        "instructors": User.objects.filter(role="instructor").count(),
        "courses": Course.objects.count(),
        "enrollments": Enrollment.objects.count(),
        "quiz_attempts": QuizAttempt.objects.count(),
        "avg_quiz_score": QuizAttempt.objects.aggregate(
            avg=__import__("django.db.models", fromlist=["Avg"]).Avg("score")
        )["avg"] or 0,
        "feedback_count": Feedback.objects.count(),
    })
