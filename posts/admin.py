from django.contrib import admin
from .models import Post, Like

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('profile', 'content', 'created_at', 'likes_count', 'shares_count', 'comments_count')
    search_fields = ('profile__user__username', 'content')
    list_filter = ('created_at',)
    readonly_fields = ('likes_count', 'shares_count', 'comments_count')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('profile', 'post', 'created_at')
    search_fields = ('profile__user__username', 'post__content')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)
