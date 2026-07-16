from django import forms
from .models import Mark, Student, Parent

class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['student', 'subject', 'assessment', 'score', 'max_score']


class ParentSignupForm(forms.Form):
    admission_number = forms.CharField(max_length=20)
    verification_code = forms.CharField(max_length=10)
    full_name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=20)
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput)