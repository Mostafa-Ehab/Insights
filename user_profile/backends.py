from typing import Any
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest

from .models import User

class EmailAuthenticationBackend(ModelBackend):
    def authenticate(self, request: HttpRequest, username=None, password=None, *args, **kwargs):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            
            return None
        except ObjectDoesNotExist:
            return None
        
    def get_user(self, user_id: int) -> AbstractBaseUser | None:
        try:
            user = User.objects.get(pk=user_id)
            return user
        
        except ObjectDoesNotExist:
            return None
        
