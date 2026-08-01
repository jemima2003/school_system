from django import forms
from .models import Mark, Student, Parent, School, Teacher, Accountant


class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['student', 'subject', 'assessment', 'score', 'max_score']


class ParentSignupForm(forms.Form):
    school = forms.ModelChoiceField(queryset=School.objects.all(), label="Select School")
    admission_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': "Child's Admission Number"})
    )
    verification_code = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={'placeholder': "Verification Code"})
    )
    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': "Your Full Name"})
    )
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': "Phone Number"})
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'placeholder': "Email (optional)"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': "Create a Password"})
    )


class SchoolSignupForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': "School Name"})
    )
    level = forms.ChoiceField(choices=School.LEVEL_CHOICES)
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': "School Email"})
    )
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': "Phone Number"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': "Create a Password"})
    )


class TeacherSignupForm(forms.Form):
    school_id = forms.IntegerField(widget=forms.HiddenInput)
    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': "Your Full Name"})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': "Email"})
    )
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': "Phone Number"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': "Create a Password"})
    )
    grade = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': "Grade You Teach (e.g. 1)"})
    )


class AccountantSignupForm(forms.Form):
    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': "Your Full Name"})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': "Email"})
    )
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': "Phone Number"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': "Create a Password"})
    )
class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': "Registered Email"}))
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': "Registered Phone Number"}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': "New Password"}))