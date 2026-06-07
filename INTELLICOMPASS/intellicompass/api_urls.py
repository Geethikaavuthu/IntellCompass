from django.urls import path, include

urlpatterns = [
    path("accounts/", include("accounts.api_urls")),
    path("courses/", include("courses.api_urls")),
    path("quizzes/", include("quizzes.api_urls")),
    path("monitoring/", include("monitoring.api_urls")),
    path("analytics/", include("analytics.api_urls")),
    path("feedback/", include("feedback.api_urls")),
    path("recommendations/", include("recommendations.api_urls")),
]
