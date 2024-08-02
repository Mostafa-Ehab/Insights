from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed

from .models import Blog, Comment, Reply
from user_profile.models import Follow, User
from notification.models import Notification


@receiver(post_save, sender=Blog)
def send_notification_to_follower_when_blog_created(instance, created,  *args, **kwargs):
    if created:
        for follower in instance.author.user_followers.all():
            Notification.objects.create(
                content_object=instance,
                user=follower.follower,
                creator=instance.author,
                notification_type="Blog"
            )


@receiver(post_save, sender=Follow)
def send_notification_to_author_when_someone_follows(instance, created, *args, **kwargs):
    if created:
        Notification.objects.create(
            content_object=instance,
            user=instance.followed,
            creator=instance.follower,
            notification_type="Follow"
        )

@receiver(m2m_changed, sender=Blog.like.through)
def send_notification_to_author_when_someone_likes_blog(instance, pk_set, action, *args, **kwargs):
    if action == "post_add":
        Notification.objects.create(
            content_object=instance,
            user=instance.author,
            creator=User.objects.get(pk=list(pk_set)[0]),
            notification_type="Like"
        )

@receiver(post_save, sender=Comment)
def send_notification_to_author_when_someone_comments(instance, created, *args, **kwargs):
    if created:
        Notification.objects.create(
            content_object=instance,
            user=instance.blog.author,
            creator=instance.user,
            notification_type="Comment"
        )

@receiver(post_save, sender=Reply)
def send_notification_to_author_when_someone_comments(instance, created, *args, **kwargs):
    if created:
        Notification.objects.create(
            content_object=instance,
            user=instance.comment.user,
            creator=instance.user,
            notification_type="Reply"
        )
