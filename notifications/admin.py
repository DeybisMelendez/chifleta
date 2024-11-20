from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("profile", "notification_type",
                    "post", "created_at", "is_read")
    search_fields = ("profile__user__username", "notification_type")
    list_filter = ("notification_type", "is_read", "created_at")
    readonly_fields = ("created_at",)
