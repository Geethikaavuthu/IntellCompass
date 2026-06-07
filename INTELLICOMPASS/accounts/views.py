from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, EmailMultiAlternatives
import logging
from django.core.cache import cache
import random
import datetime
from django.utils import timezone
from .forms import RegisterForm, ProfileForm
from .models import User
from courses.models import Course, Enrollment
from quizzes.models import QuizAttempt
from feedback.models import Feedback
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import authenticate

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Create an inactive user and send activation email
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Send a one-time 6-digit OTP to user's email for verification
            if user.email:
                otp = f"{random.randint(0, 999999):06d}"
                # store otp in cache for 15 minutes
                cache_key = f"otp_user_{user.pk}"
                cache.set(cache_key, {'otp': otp, 'created': timezone.now().isoformat()}, timeout=15 * 60)

                subject = "Your IntelliCompass verification code"
                message = render_to_string('accounts/otp_email.html', {
                    'user': user,
                    'otp': otp,
                })
                # send multipart email (HTML + plain text)
                text_message = f"Your verification code is: {otp}\nThis code expires in 15 minutes."
                email_msg = EmailMultiAlternatives(subject, text_message, settings.DEFAULT_FROM_EMAIL, [user.email])
                email_msg.attach_alternative(message, "text/html")
                try:
                    email_msg.send(fail_silently=False)
                    logging.getLogger('accounts').info('Sent OTP to user %s (id=%s)', user.email, user.pk)
                except Exception as exc:
                    logging.getLogger('accounts').exception('Failed sending OTP to user %s: %s', user.email, exc)
                    messages.warning(request, "Could not send verification email — please contact support.")

            messages.success(request, "Account created — a verification code has been sent to your email.")
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            return redirect('accounts:verify_otp', uidb64=uid)
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def activation_sent_view(request):
    return render(request, 'accounts/activation_sent.html')


def activate_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Your account has been activated.')
        return redirect('accounts:dashboard')
    else:
        return render(request, 'accounts/activation_invalid.html')


def verify_otp_view(request, uidb64):
    """Verify OTP sent to user's email after registration."""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user is None:
        messages.error(request, "Invalid verification request.")
        return redirect('accounts:register')

    # compute resend cooldown remaining
    cooldown_key = f"resend_last_user_{user.pk}"
    resend_remaining = 0
    last = cache.get(cooldown_key)
    cooldown_seconds = 60
    if last:
        try:
            last_dt = datetime.datetime.fromisoformat(last)
            last_dt = timezone.datetime.fromisoformat(last)
            elapsed = (timezone.now() - last_dt).total_seconds()
            resend_remaining = int(max(0, cooldown_seconds - elapsed))
        except Exception:
            resend_remaining = 0

    if request.method == 'POST':
        code = request.POST.get('otp', '').strip()
        cache_key = f"otp_user_{user.pk}"
        data = cache.get(cache_key)

        # attempt limiting
        attempts_key = f"otp_attempts_user_{user.pk}"
        attempts = cache.get(attempts_key) or 0
        max_attempts = 5

        if data and data.get('otp') == code:
            user.is_active = True
            user.save()
            cache.delete(cache_key)
            cache.delete(attempts_key)
            login(request, user)
            messages.success(request, 'Your account has been verified.')
            return redirect('accounts:dashboard')
        else:
            logging.getLogger('accounts').warning('Failed OTP attempt for user id=%s (attempt %s)', user.pk, attempts + 1)
            attempts += 1
            cache.set(attempts_key, attempts, timeout=15 * 60)
            if attempts >= max_attempts:
                messages.error(request, 'Too many failed attempts. Please request a new code.')
            else:
                messages.error(request, 'Invalid or expired verification code.')

    return render(request, 'accounts/verify_otp.html', {
        'user': user,
        'uidb64': uidb64,
        'resend_remaining': resend_remaining,
    })

def login_view(request):
    from django.contrib.auth.forms import AuthenticationForm
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Update streak
            from django.utils import timezone
            today = timezone.now().date()
            if user.last_active:
                diff = (today - user.last_active).days
                if diff == 1:
                    user.streak_days += 1
                elif diff > 1:
                    user.streak_days = 1
            else:
                user.streak_days = 1
            user.last_active = today
            user.save()
            return redirect("accounts:dashboard")
        else:
            # If authentication failed, check if the account exists but is inactive
            username = request.POST.get('username')
            candidate = None
            if username:
                try:
                    candidate = User.objects.filter(username__iexact=username).first()
                    if not candidate:
                        candidate = User.objects.filter(email__iexact=username).first()
                except Exception:
                    candidate = None
            if candidate and not candidate.is_active:
                uid = urlsafe_base64_encode(force_bytes(candidate.pk))
                messages.warning(request, 'Account not activated. Enter the code sent to your email or request a new one.')
                return redirect('accounts:verify_otp', uidb64=uid)
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})


def resend_otp_view(request, uidb64):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        messages.error(request, "Invalid request to resend code.")
        return redirect('accounts:register')

    # rate limiting: max 5 resends per day
    resend_count_key = f"resend_count_user_{user.pk}"
    resend_count = cache.get(resend_count_key) or 0
    max_resend_per_day = 5
    if resend_count >= max_resend_per_day:
        messages.error(request, "You've reached the maximum number of resends for today.")
        return redirect('accounts:verify_otp', uidb64=uidb64)

    cooldown_key = f"resend_last_user_{user.pk}"
    last = cache.get(cooldown_key)
    cooldown_seconds = 60
    if last:
        try:
            last_dt = timezone.datetime.fromisoformat(last)
            elapsed = (timezone.now() - last_dt).total_seconds()
            remaining = int(max(0, cooldown_seconds - elapsed))
        except Exception:
            remaining = cooldown_seconds
        if remaining > 0:
            messages.error(request, f"Please wait {remaining}s before resending the code.")
            return redirect('accounts:verify_otp', uidb64=uidb64)

    # generate and send new OTP
    otp = f"{random.randint(0, 999999):06d}"
    cache_key = f"otp_user_{user.pk}"
    now_iso = timezone.now().isoformat()
    cache.set(cache_key, {'otp': otp, 'created': now_iso}, timeout=15 * 60)
    cache.set(cooldown_key, now_iso, timeout=cooldown_seconds)
    cache.set(resend_count_key, resend_count + 1, timeout=24 * 3600)
    subject = "Your IntelliCompass verification code"
    message = render_to_string('accounts/otp_email.html', {
        'user': user,
        'otp': otp,
    })
    text_message = f"Your verification code is: {otp}\nThis code expires in 15 minutes."
    email_msg = EmailMultiAlternatives(subject, text_message, settings.DEFAULT_FROM_EMAIL, [user.email])
    email_msg.attach_alternative(message, 'text/html')
    try:
        email_msg.send(fail_silently=False)
        logging.getLogger('accounts').info('Resent OTP to user %s (id=%s); count=%s', user.email, user.pk, resend_count + 1)
    except Exception as exc:
        logging.getLogger('accounts').exception('Failed resending OTP to %s: %s', user.email, exc)
        messages.warning(request, 'Could not send verification email — please contact support.')

    messages.success(request, 'A new verification code has been sent to your email.')
    return redirect('accounts:verify_otp', uidb64=uidb64)

def logout_view(request):
    logout(request)
    return redirect("home")

@login_required
def dashboard_view(request):
    user = request.user
    context = {}

    if user.is_student():
        enrollments = Enrollment.objects.filter(student=user).select_related("course")
        attempts = QuizAttempt.objects.filter(student=user).order_by("-completed_at")[:5]
        context.update({
            "enrollments": enrollments,
            "recent_attempts": attempts,
            "streak": user.streak_days,
        })
        return render(request, "accounts/student_dashboard.html", context)

    elif user.is_instructor():
        courses = Course.objects.filter(instructor=user)
        total_students = Enrollment.objects.filter(course__instructor=user).count()
        context.update({
            "courses": courses,
            "total_students": total_students,
        })
        return render(request, "accounts/instructor_dashboard.html", context)

    elif user.is_admin_user():
        context.update({
            "total_students": User.objects.filter(role="student").count(),
            "total_instructors": User.objects.filter(role="instructor").count(),
            "total_courses": Course.objects.count(),
            "total_enrollments": Enrollment.objects.count(),
            "recent_feedback": Feedback.objects.order_by("-created_at")[:10],
        })
        return render(request, "accounts/admin_dashboard.html", context)

    return render(request, "accounts/dashboard_generic.html", context)

@login_required
def profile_view(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("accounts:profile")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "accounts/profile.html", {"form": form})


@csrf_exempt
def firebase_login_view(request):
    """Endpoint to accept a Firebase ID token from the client and log the user in.

    Client should POST JSON: {"idToken": "<firebase_id_token>"}
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)
    try:
        payload = json.loads(request.body.decode('utf8'))
        id_token = payload.get('idToken')
    except Exception:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    if not id_token:
        return JsonResponse({'error': 'idToken required'}, status=400)

    # Use the FirebaseBackend to authenticate
    user = authenticate(request, firebase_token=id_token)
    if user is None:
        return JsonResponse({'error': 'Invalid or expired token'}, status=401)

    # Log the user in into the Django session
    login(request, user)
    return JsonResponse({'status': 'ok', 'next': reverse('accounts:dashboard')})
