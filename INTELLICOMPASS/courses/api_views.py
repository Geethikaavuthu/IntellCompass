from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Course, Enrollment

@api_view(["GET"])
@permission_classes([AllowAny])
def course_list_api(request):
    courses = Course.objects.filter(is_published=True).values(
        "id", "title", "description", "category", "instructor__username", "created_at"
    )
    return Response(list(courses))

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def course_detail_api(request, pk):
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response({"error": "Not found"}, status=404)
    lessons = list(course.lessons.values("id", "title", "content_type", "order"))
    enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()
    return Response({
        "id": course.id,
        "title": course.title,
        "description": course.description,
        "instructor": course.instructor.username,
        "lessons": lessons,
        "enrolled": enrolled,
    })
