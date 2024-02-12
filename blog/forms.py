# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.db.models.functions import datetime

from .models import User, Post


# for class based views
class RegisterForm(UserCreationForm):
    pass


#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']
#
#
# class LoginForm(AuthenticationForm):
#     pass

# for funcition based views
class LoginForm(forms.Form):
    username = forms.CharField(max_length=28)
    password = forms.CharField(max_length=28)


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(max_length=28, widget=forms.TextInput(
        attrs={"id": "password", "type": "password"}))
    password2 = forms.CharField(max_length=28, widget=forms.TextInput(
        attrs={"id": "password", "type": "password"}))

    avatar = forms.FileField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    def save(self, commit=True):
        user = super().save(commit)
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 == p2:
            user.set_password(p1)
            user.save()
        else:
            raise ValidationError("Passwords do not match!")

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password1", "password2", "avatar"]


class PostCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control", "placeholder": f"Enter the {field}"})

    class Meta:
        model = Post
        fields = ["title", "content", "is_active"]


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "is_active"]
