from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Feedback

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def feedback_list(request):
    feedbacks = Feedback.objects.order_by("-created_at")[:50].values(
        "id", "student__username", "course__title", "rating", "comment", "created_at"
    )
    return Response(list(feedbacks))
