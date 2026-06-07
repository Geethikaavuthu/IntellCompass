from django import forms
from .models import Course, Lesson

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["title", "description", "category", "thumbnail", "is_published"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "category": forms.TextInput(attrs={"class": "form-control"}),
            "thumbnail": forms.FileInput(attrs={"class": "form-control"}),
            "is_published": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ["title", "content_type", "text_content", "video_url", "pdf_file", "order"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content_type": forms.Select(attrs={"class": "form-select"}),
            "text_content": forms.Textarea(attrs={"class": "form-control", "rows": 8}),
            "video_url": forms.URLInput(attrs={"class": "form-control"}),
            "pdf_file": forms.FileInput(attrs={"class": "form-control"}),
            "order": forms.NumberInput(attrs={"class": "form-control"}),
        }
