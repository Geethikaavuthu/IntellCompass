from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.Select(choices=[(i,f"{i} ★") for i in range(1,6)], attrs={"class": "form-select"}),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Your feedback..."}),
        }
