from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import Follow, Profile
from posts.models import Post, Like


@receiver(post_save, sender=Like)
def create_notification_for_like(sender, instance, created, **kwargs):
    if created and instance.profile.pk != instance.post.profile.pk:
        notification = Notification.objects.create(
            notification_type="like", follower=instance.profile, profile=instance.post.profile, post=instance.post)
        notification.save()

@receiver(post_save, sender=Follow)
def create_notification_for_follow(sender, instance, created, **kwargs):
    if created and instance.follower.pk != instance.followed.pk:
        notification = Notification.objects.create(
            notification_type="follow", follower=instance.follower, profile=instance.followed)
        notification.save()


@receiver(post_save, sender=Post)
def create_notification_for_post(sender, instance, created, **kwargs):
    if created:
        if instance.parent:
            if instance.profile.pk != instance.parent.profile:
                notification = Notification.objects.create(
                    notification_type="comment", post=instance, profile=instance.parent.profile)
                notification.save()
        if instance.share:
            if instance.profile.pk != instance.share.profile:
                notification = Notification.objects.create(
                    notification_type="share", post=instance, profile=instance.share.profile)
                notification.save()


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ("comment", "Comment"),
        ("like", "Like"),
        ("share", "Share"),
        ("follow", "Follow"),
    ]
    follower = models.ForeignKey(
        Profile, null=True, blank=True, related_name="followers", on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    notification_type = models.CharField(
        max_length=10, choices=NOTIFICATION_TYPES)
    post = models.ForeignKey(
        Post, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.profile.user.username}: {self.notification_type} at {self.created_at}"
