from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def current_user(request):
    u = request.user
    return Response({
        "id": u.id,
        "username": u.username,
        "email": u.email,
        "role": u.role,
        "first_name": u.first_name,
        "last_name": u.last_name,
        "streak_days": u.streak_days,
    })
