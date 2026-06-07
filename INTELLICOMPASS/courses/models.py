from django.db import models
from django.conf import settings

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="courses_taught")
    thumbnail = models.ImageField(upload_to="course_thumbnails/", blank=True, null=True)
    category = models.CharField(max_length=100, blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def enrolled_count(self):
        return self.enrollments.count()

    def lesson_count(self):
        return self.lessons.count()

class Lesson(models.Model):
    class ContentType(models.TextChoices):
        TEXT = "text", "Text"
        VIDEO = "video", "Video"
        PDF = "pdf", "PDF"

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)
    content_type = models.CharField(max_length=10, choices=ContentType.choices, default=ContentType.TEXT)
    text_content = models.TextField(blank=True)
    video_url = models.URLField(blank=True)
    pdf_file = models.FileField(upload_to="lesson_pdfs/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    enrolled_at = models.DateTimeField(auto_now_add=True)
    progress = models.FloatField(default=0.0)  # 0-100
    completed_lessons = models.ManyToManyField(Lesson, blank=True, related_name="completed_by")

    class Meta:
        unique_together = ["student", "course"]

    def __str__(self):
        return f"{self.student.username} → {self.course.title}"

    def update_progress(self):
        total = self.course.lessons.count()
        if total > 0:
            self.progress = (self.completed_lessons.count() / total) * 100
            self.save()
