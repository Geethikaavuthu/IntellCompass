from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Lesson, Enrollment
from .forms import CourseForm, LessonForm

def course_list(request):
    courses = Course.objects.filter(is_published=True).select_related("instructor")
    return render(request, "courses/course_list.html", {"courses": courses})

@login_required
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    enrollment = None
    if request.user.is_student():
        enrollment = Enrollment.objects.filter(student=request.user, course=course).first()
    return render(request, "courses/course_detail.html", {"course": course, "enrollment": enrollment})

@login_required
def enroll(request, pk):
    course = get_object_or_404(Course, pk=pk, is_published=True)
    if request.user.is_student():
        Enrollment.objects.get_or_create(student=request.user, course=course)
        messages.success(request, f"Enrolled in {course.title}!")
    return redirect("courses:detail", pk=pk)

@login_required
def lesson_view(request, course_pk, lesson_pk):
    course = get_object_or_404(Course, pk=course_pk)
    lesson = get_object_or_404(Lesson, pk=lesson_pk, course=course)
    enrollment = None
    if request.user.is_student():
        enrollment = Enrollment.objects.filter(student=request.user, course=course).first()
    return render(request, "courses/lesson_view.html", {
        "course": course, "lesson": lesson, "enrollment": enrollment,
    })

@login_required
def mark_lesson_complete(request, course_pk, lesson_pk):
    if request.method == "POST" and request.user.is_student():
        enrollment = get_object_or_404(Enrollment, student=request.user, course_id=course_pk)
        lesson = get_object_or_404(Lesson, pk=lesson_pk, course_id=course_pk)
        enrollment.completed_lessons.add(lesson)
        enrollment.update_progress()
        messages.success(request, "Lesson marked as complete!")
    return redirect("courses:lesson", course_pk=course_pk, lesson_pk=lesson_pk)

@login_required
def create_course(request):
    if not request.user.is_instructor():
        return redirect("accounts:dashboard")
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            messages.success(request, "Course created!")
            return redirect("courses:manage", pk=course.pk)
    else:
        form = CourseForm()
    return render(request, "courses/create_course.html", {"form": form})

@login_required
def manage_course(request, pk):
    course = get_object_or_404(Course, pk=pk, instructor=request.user)
    lessons = course.lessons.all()
    return render(request, "courses/manage_course.html", {"course": course, "lessons": lessons})

@login_required
def add_lesson(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk, instructor=request.user)
    if request.method == "POST":
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            messages.success(request, "Lesson added!")
            return redirect("courses:manage", pk=course_pk)
    else:
        form = LessonForm()
    return render(request, "courses/add_lesson.html", {"form": form, "course": course})
