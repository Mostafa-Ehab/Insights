from django.urls import path

from .views import *

urlpatterns = [
    path('login', login_view, name="login"),
    path('register', register_view, name="register"),
    path('logout', logout_view, name="logout")
]

