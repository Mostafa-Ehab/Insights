from django.http import HttpRequest
from .models import Notification

def user_notifications(request: HttpRequest):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(
            user=request.user
        ).order_by("-created_date")
        unseen = notifications.exclude(is_seen=True).count()

    return {
        "notifications": notifications,
        "unseen_num": unseen
    }
