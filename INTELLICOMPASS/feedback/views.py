from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from courses.models import Course
from .models import Feedback
from .forms import FeedbackForm

@login_required
def submit_feedback(request, course_pk):
    if request.method == "POST":
        course = get_object_or_404(Course, pk=course_pk)
        form = FeedbackForm(request.POST)
        if form.is_valid():
            fb = form.save(commit=False)
            fb.student = request.user
            fb.course = course
            fb.save()
            messages.success(request, "Feedback submitted!")
    return redirect("courses:detail", pk=course_pk)
