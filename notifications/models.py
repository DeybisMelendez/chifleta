from django.db import models
from accounts.models import Profile
from posts.models import Post

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('comment', 'Comment'),
        ('like', 'Like'),
        ('share', 'Share'),
        ('follow', 'Follow'),
    ]
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.account.user.username}: {self.notification_type} at {self.created_at}"
