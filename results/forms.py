from django import forms
from .models import Mark, Student, Parent, School, Teacher, Accountant


class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['student', 'subject', 'assessment', 'score', 'max_score']


class ParentSignupForm(forms.Form):
    school = forms.ModelChoiceField(queryset=School.objects.all(), label="Select School")
    admission_number = forms.CharField(max_length=20)
    verification_code = forms.CharField(max_length=10)
    full_name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=20)
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput)


class SchoolSignupForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)


class TeacherSignupForm(forms.Form):
    school_id = forms.IntegerField(widget=forms.HiddenInput)
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)
    grade = forms.IntegerField()


class AccountantSignupForm(forms.Form):
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)