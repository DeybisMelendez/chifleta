from django.contrib import admin

from .models import Follow, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "followers_count", "following_count", "created_at")
    search_fields = ("user__username", "bio")
    list_filter = ("created_at",)
    readonly_fields = ("followers_count", "following_count",)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("follower", "followed", "followed_at")
    search_fields = ("follower__user__username", "followed__user__username")
    list_filter = ("followed_at",)
    readonly_fields = ("followed_at",)
