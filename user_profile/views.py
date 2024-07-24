from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.urls import reverse
from django.contrib.auth import authenticate, logout, login
from .forms import LoginForm, RegisterForm
from .models import User

# Create your views here.
def login_view(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect(reverse("home"))
    
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get("username"),
                password=form.cleaned_data.get("password")
            )
            if user:
                login(request, user)
                return redirect(reverse("home"))
            else:
                form.add_error(None, "Incorrect username or password")
        
    return render(request, "pages/login.html", {
        "login_form": form
    })


def register_view(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect(reverse("home"))
    
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get("password"))
            user.save()

            login(request, user)

            return redirect(reverse("home"))
        print(form.errors)

    return render(request, "pages/register.html", {
        "register_form": form
    })

def logout_view(request: HttpRequest):
    logout(request)
    print("logged out")
    return redirect(reverse("home"))
