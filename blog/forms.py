from django import forms
from .models import Thread

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ["body"]
        widgets = {
            "body": forms.TextInput(attrs={
                "class": "form-control form-control-lg border-danger",
                "placeholder": "What's on your mind?",
            }),
        }