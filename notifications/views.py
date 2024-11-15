from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import Notification


@login_required(redirect_field_name="log_in")
def notifications(request):
    notifications = Notification.objects.filter(profile__user=request.user)
    for notification in notifications:
        notification.is_read = True
        notification.save()
    context = {
        "notifications": notifications
    }

    return render(request, "notifications.html", context)


@login_required(redirect_field_name="log_in")
def check_notification(_, pk):

    notifications = Notification.objects.filter(pk=pk)
    if not notifications.exists():
        return redirect("feed")
    notification = notifications.first()
    notification.is_read = True

    notification.save()

    return redirect("post", notification.post.pk)


def check_all_notification(request):

    notifications = Notification.objects.filter(profile__user=request.user)

    for notification in notifications:
        notification.is_read = True
        notification.save()

    return redirect("notification")


def notifications_button(request):

    has_notifications= Notification.objects.filter(profile__user=request.user, is_read=False).exists()
    context={
        "has_notifications": has_notifications
    }
    
    return render(request, "htmx/notification_button.html", context)
