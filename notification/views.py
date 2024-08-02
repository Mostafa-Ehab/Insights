from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest, Http404, HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Notification

# Create your views here.
@login_required(login_url="/login")
def notification_redirect(request: HttpRequest, notification_id: int):
    if (notification := Notification.objects.get(pk=notification_id)):
        if request.user == notification.user:
            
            notification.is_seen = True
            notification.save()
            if notification.notification_type == "Follow":
                return redirect(reverse("profile"))
            
            elif notification.notification_type in ["Blog", "Like"]:
                return redirect(reverse("post", kwargs={"slug": notification.content_object.slug}))
            
            return redirect("/")
        else:
            return HttpResponseForbidden()
    else:
        return Http404()
    

@login_required(login_url="/login")
def notifications_seen(request: HttpRequest):
    for notification in Notification.objects.filter(user=request.user):
        notification.is_seen = True
        notification.save()

    return JsonResponse({
        "code": 200
    })
