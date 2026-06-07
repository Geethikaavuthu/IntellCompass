from django.core.management.base import BaseCommand
from accounts.models import User
from courses.models import Course, Lesson, Enrollment
from quizzes.models import Quiz, Question

class Command(BaseCommand):
    help = "Seed database with sample data"

    def handle(self, *args, **options):
        # Create users
        admin_user, _ = User.objects.get_or_create(
            username="admin", defaults={"role": "admin", "email": "admin@intellicompass.com", "is_staff": True}
        )
        admin_user.set_password("admin123")
        admin_user.save()

        instructor, _ = User.objects.get_or_create(
            username="instructor1", defaults={"role": "instructor", "email": "instructor@intellicompass.com", "first_name": "Dr. Sarah", "last_name": "Johnson"}
        )
        instructor.set_password("instructor123")
        instructor.save()

        student, _ = User.objects.get_or_create(
            username="student1", defaults={"role": "student", "email": "student@intellicompass.com", "first_name": "Alex", "last_name": "Chen"}
        )
        student.set_password("student123")
        student.save()

        # Create courses
        course1, _ = Course.objects.get_or_create(
            title="Python Programming Fundamentals",
            defaults={"description": "Learn Python from scratch with hands-on projects.", "instructor": instructor, "category": "Programming", "is_published": True}
        )
        course2, _ = Course.objects.get_or_create(
            title="Machine Learning Basics",
            defaults={"description": "Introduction to ML concepts and algorithms.", "instructor": instructor, "category": "Data Science", "is_published": True}
        )

        # Create lessons
        for i, title in enumerate(["Variables & Data Types", "Control Flow", "Functions", "OOP Basics"], 1):
            Lesson.objects.get_or_create(course=course1, title=title, defaults={"content_type": "text", "text_content": f"Lesson content for {title}...", "order": i})

        for i, title in enumerate(["What is ML?", "Linear Regression", "Classification"], 1):
            Lesson.objects.get_or_create(course=course2, title=title, defaults={"content_type": "text", "text_content": f"Lesson content for {title}...", "order": i})

        # Enroll student
        Enrollment.objects.get_or_create(student=student, course=course1)

        # Create quiz
        quiz, _ = Quiz.objects.get_or_create(course=course1, title="Python Basics Quiz", defaults={"description": "Test your Python knowledge"})
        Question.objects.get_or_create(quiz=quiz, text="What is the output of print(2**3)?", defaults={
            "option_a": "6", "option_b": "8", "option_c": "9", "option_d": "5", "correct_answer": "B", "difficulty": "easy", "explanation": "2**3 = 2^3 = 8", "order": 1
        })
        Question.objects.get_or_create(quiz=quiz, text="Which keyword defines a function in Python?", defaults={
            "option_a": "func", "option_b": "function", "option_c": "def", "option_d": "define", "correct_answer": "C", "difficulty": "easy", "explanation": "The def keyword is used to define functions.", "order": 2
        })
        Question.objects.get_or_create(quiz=quiz, text="What type is the result of 10/3 in Python 3?", defaults={
            "option_a": "int", "option_b": "float", "option_c": "str", "option_d": "double", "correct_answer": "B", "difficulty": "medium", "explanation": "Division always returns float in Python 3.", "order": 3
        })

        self.stdout.write(self.style.SUCCESS("✅ Sample data seeded successfully!"))
        self.stdout.write(f"   Admin: admin / admin123")
        self.stdout.write(f"   Instructor: instructor1 / instructor123")
        self.stdout.write(f"   Student: student1 / student123")
