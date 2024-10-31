from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to="avatars/", default="avatars/default_avatar.png", null=True, blank=True)
    bio = models.TextField(max_length=512, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    followers_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)

    def toggle_follow(self, profile):
        """
        Alterna el seguimiento de otro perfil. Si ya lo sigue, lo deja de seguir.
        Si no lo sigue, empieza a seguirlo.
        """
        follow, created = Follow.objects.get_or_create(
            follower=self, followed=profile)
        if not created:
            follow.delete()

    def update_follow_counts(self):
        """
        Actualiza los contadores de seguidores y seguidos de este perfil.
        """
        self.followers_count = Follow.objects.filter(followed=self).count()
        self.following_count = Follow.objects.filter(follower=self).count()
        self.save()

    def delete(self, *args, **kwargs):
        """
        Sobreescribe el método delete para eliminar todas las relaciones de seguimiento
        relacionadas con este perfil y actualizar los contadores de los otros perfiles.
        """
        Follow.objects.filter(follower=self).delete()
        Follow.objects.filter(followed=self).delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.user.username


class Follow(models.Model):
    follower = models.ForeignKey(
        Profile, related_name="following", on_delete=models.CASCADE)
    followed = models.ForeignKey(
        Profile, related_name="followers", on_delete=models.CASCADE)
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "followed")

    def __str__(self):
        return f"{self.follower} follows {self.followed}"

    def save(self, *args, **kwargs):
        """
        Sobreescribimos el método save para actualizar los contadores de seguidores y seguidos.
        """
        super().save(*args, **kwargs)
        self.follower.update_follow_counts()
        self.followed.update_follow_counts()

    def delete(self, *args, **kwargs):
        """
        Sobreescribimos el método delete para actualizar los contadores de seguidores y seguidos.
        """
        super().delete(*args, **kwargs)
        self.follower.update_follow_counts()
        self.followed.update_follow_counts()
