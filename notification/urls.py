from django.urls import path

from .views import *

urlpatterns = [
    path("open/<int:notification_id>", notification_redirect, name="open_notification"),
    path("seen", notifications_seen, name="notifications_seen")
]
