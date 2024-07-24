from django import forms
from django.contrib.auth import authenticate

from .models import User

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your username or email"
            }))
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your password"
            }))


class RegisterForm(forms.ModelForm):
    conf_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Confirm your password"
        })
    )

    class Meta:
        model = User
        fields = ("username", "email", "password")

        widgets = {
            "username": forms.TextInput(attrs={
                    "class": "form-control",
                    "placeholder": "Enter your username"
                }),
            "email": forms.EmailInput(attrs={
                    "class": "form-control",
                    "placeholder": "Enter your email"
                }),
            "password": forms.PasswordInput(attrs={
                    "class": "form-control",
                    "placeholder": "Enter your password"
                })
        }

    def clean_username(self):
        username = self.cleaned_data.get("username")
        model = self.Meta.model
        user = model.objects.filter(username__iexact=username)

        if user.exists():
            raise forms.ValidationError("A user with that name already exist")

        return username
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        model = self.Meta.model
        user = model.objects.filter(email__iexact=email)

        if user.exists():
            raise forms.ValidationError("This email already exist try login instead")

        return email
    
    def clean(self):
        if self.is_valid():
            password = self.cleaned_data.get("password")
            password2 = self.cleaned_data.get("conf_password")
            if password != password2:
                raise forms.ValidationError("Passwords don't match")

        return self.cleaned_data

    