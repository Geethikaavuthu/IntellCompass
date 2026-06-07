import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.conf import settings
from .models import Quiz, Question, QuizAttempt

@login_required
def quiz_list(request, course_pk):
    quizzes = Quiz.objects.filter(course_id=course_pk)
    return render(request, "quizzes/quiz_list.html", {"quizzes": quizzes, "course_pk": course_pk})

@login_required
def take_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    questions = quiz.questions.all()
    if request.method == "POST":
        correct = 0
        total = questions.count()
        answers = {}
        for q in questions:
            ans = request.POST.get(f"q_{q.id}")
            answers[str(q.id)] = ans
            if ans == q.correct_answer:
                correct += 1
        score = (correct / total * 100) if total > 0 else 0
        attempt = QuizAttempt.objects.create(
            student=request.user, quiz=quiz,
            score=round(score, 1), total_questions=total,
            correct_answers=correct, answers_json=answers,
            completed_at=timezone.now(),
        )
        return redirect("quizzes:result", pk=attempt.pk)
    return render(request, "quizzes/take_quiz.html", {"quiz": quiz, "questions": questions})

@login_required
def quiz_result(request, pk):
    attempt = get_object_or_404(QuizAttempt, pk=pk, student=request.user)
    questions = attempt.quiz.questions.all()
    results = []
    for q in questions:
        user_ans = attempt.answers_json.get(str(q.id), "")
        results.append({
            "question": q,
            "user_answer": user_ans,
            "correct": user_ans == q.correct_answer,
        })
    return render(request, "quizzes/quiz_result.html", {"attempt": attempt, "results": results})

@login_required
def generate_quiz_api(request):
    """Generate adaptive quiz questions using Gemini API."""
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)
    try:
        try:
            import google.generativeai as genai
        except ImportError:
            return JsonResponse({"error": "AI generation not available. Install optional dependency 'google-generativeai' and set GEMINI_API_KEY."}, status=501)
        body = json.loads(request.body)
        topic = body.get("topic", "General Knowledge")
        difficulty = body.get("difficulty", "medium")
        count = body.get("count", 5)
        if not settings.GEMINI_API_KEY:
            return JsonResponse({"error": "Gemini API key not configured."}, status=501)

        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""Generate {count} multiple choice questions about "{topic}" at {difficulty} difficulty level.
        Return ONLY valid JSON array. Each object must have:
        {{"text": "question", "option_a": "...", "option_b": "...", "option_c": "...", "option_d": "...", "correct_answer": "A/B/C/D", "explanation": "..."}}
        """

        response = model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0]
        questions = json.loads(text)
        return JsonResponse({"questions": questions})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
