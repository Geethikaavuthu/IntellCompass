from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("accounts/", include("accounts.urls")),
    path("courses/", include("courses.urls")),
    path("quizzes/", include("quizzes.urls")),
    path("monitoring/", include("monitoring.urls")),
    path("analytics/", include("analytics.urls")),
    path("feedback/", include("feedback.urls")),
    path("recommendations/", include("recommendations.urls")),
    path("api/", include("intellicompass.api_urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
