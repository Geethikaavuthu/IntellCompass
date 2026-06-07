from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("activate/sent/", views.activation_sent_view, name="activation_sent"),
    path("activate/<uidb64>/<token>/", views.activate_view, name="activate"),
    path("verify-otp/<uidb64>/", views.verify_otp_view, name='verify_otp'),
    path("verify-otp/<uidb64>/resend/", views.resend_otp_view, name='resend_otp'),
    # Password reset flow
    path("password-reset/", auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        success_url=reverse_lazy('accounts:password_reset_done')
    ), name='password_reset'),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html',
        success_url=reverse_lazy('accounts:password_reset_complete')
    ), name='password_reset_confirm'),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("profile/", views.profile_view, name="profile"),
    path("firebase-login/", views.firebase_login_view, name="firebase_login"),
]
