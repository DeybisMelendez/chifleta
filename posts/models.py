from django.db import models

from accounts.models import Profile


class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    # TODO: Implementar Markdown en los posts, evaluar el tamaño máximo de caracteres
    content = models.TextField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)
    # Indicaría si el post es comentario de otro post, tendría una referencia al post comentado
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE)
    # Indicaría si el post es un "retuit" o repost, tendría una referencia al post compartido
    share = models.ForeignKey(
        "self", null=True, blank=True, related_name="shares", on_delete=models.CASCADE)
    # TODO: Evaluar si se puede agregar imagenes
    image = models.ImageField(upload_to="posts/images/", null=True, blank=True)
    likes_count = models.PositiveIntegerField(default=0)
    shares_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)

    def is_comment(self):
        """Valida si el post es un comentario"""
        return self.parent is not None

    def is_shared(self):
        """Valida si el post es compartido de otro post"""
        return self.share is not None

    def save(self, *args, **kwargs):
        """Sobrescribir el método save para manejar la lógica de compartidos y comentarios."""
        super().save(*args, **kwargs)

        if self.parent:
            self.parent.comments_count += 1
            self.parent.save()

        if self.share:
            self.share.shares_count += 1
            self.share.save()

    def delete(self, *args, **kwargs):
        """Sobrescribir el método delete para manejar la lógica de eliminación de comentarios."""
        if self.parent:
            self.parent.comments_count -= 1
            self.parent.save()

        if self.share:
            self.share.shares_count -= 1
            self.share.save()

        super().delete(*args, **kwargs)

    def __str__(self):
        return f"Post by {self.profile.user.username}: {self.content[:50]}"


class Like(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Evita duplicar likes en el contador
            self.post.likes_count += 1
            self.post.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.post.likes_count -= 1
        self.post.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.profile.user.username} liked {self.post.content[:50]}"
    # TODO: Evaluar si es necesario agregar mas información al like

# TODO Evaluar si vale la pena agregar Dislike o utilizar la misma clase para likes negativos
