from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = "student", "Student"
        INSTRUCTOR = "instructor", "Instructor"
        ADMIN = "admin", "Admin"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    streak_days = models.PositiveIntegerField(default=0)
    last_active = models.DateField(null=True, blank=True)

    def is_student(self):
        return self.role == self.Role.STUDENT

    def is_instructor(self):
        return self.role == self.Role.INSTRUCTOR

    def is_admin_user(self):
        return self.role == self.Role.ADMIN

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
