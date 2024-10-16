from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # TODO: Configurar bien la carpeta avatars y el default_avatar.png
    # avatar = models.ImageField(upload_to="avatars/", default="avatars/default_avatar.png", null=True, blank=True)
    bio = models.TextField(max_length=512, blank=True)
    follows = models.ManyToManyField("self", symmetrical=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    followers_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)

    def toggle_follow(self, account):
        """
        Alterna el seguimiento de otra cuenta. Si la está siguiendo, deja de seguirla.
        Si no la está siguiendo, la sigue.
        Actualiza los contadores de seguidores y seguidos automáticamente.
        """
        if self.follows.filter(id=account.id).exists():
            self.follows.remove(account)
        else:
            self.follows.add(account)

        self.update_follow_counts()
        account.update_follow_counts()

    def update_follow_counts(self):
        """
        Actualiza el total de seguidores y seguidos.
        """
        self.followers_count = Account.objects.filter(follows=self).count()
        self.following_count = self.follows.count()
        self.save()
    
    def __str__(self):
        return self.user.username

