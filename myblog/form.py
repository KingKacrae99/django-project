from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Post, Comment, UserSettings

class LoginForm(forms.Form):
    username = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                "class": "form-control"
            }
        )
    )

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                "class": "form-control"
            }
        )
    )
    email = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                "class": "form-control"
            }
        )
    )
    password1 = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                "class": "form-control"
            }
        )
    )
    password2 = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                "class": "form-control"
            }
        )
    )


    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['likes','slug','status','dop']

class PrivacySettingForm(forms.Form):
    show_email = forms.BooleanField(
        widget = forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'
                }
            )
    )
    allow_view = forms.BooleanField(
        widget= forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'
                }
        )
    )
