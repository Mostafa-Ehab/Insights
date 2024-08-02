from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from user_profile.models import User
from utils import datetime_format

# Create your models here.
class Notification(models.Model):
    NOTIFICATION_TYPE = ("Blog", "Follow", "Like", "Comment", "Reply")

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )

    object_id = models.BigIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey(
        User,
        related_name="user_notifications",
        on_delete=models.CASCADE
    )
    creator = models.ForeignKey(
        User,
        related_name="user_notifications_send",
        on_delete=models.CASCADE
    )

    is_seen = models.BooleanField(default=False)

    notification_type = models.CharField(
        max_length=20,
        choices=list(zip(NOTIFICATION_TYPE, NOTIFICATION_TYPE))
    )

    created_date = models.DateTimeField(auto_now_add=True)

    def text(self):
        if self.notification_type == "Follow":
            return f"{self.creator.username} started following you"
        
        elif self.notification_type == "Blog":
            return f"{self.creator.username} posted a new blog"
        
        elif self.notification_type == "Like":
            return f"{self.creator.username} liked your blog"
        
        elif self.notification_type == "Comment":
            return f"{self.creator.username} commented on your blog"
        
        elif self.notification_type == "Reply":
            return f"You have a new reply from {self.creator.username}"

    def formatted_date(self):
        return datetime_format(self.created_date)

    def __str__(self):
        return self.text()
