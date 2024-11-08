from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from accounts.models import Profile

from .models import Notification

# Create your views here.


@login_required(redirect_field_name="log_in")
def notification(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    notifications = Notification.objects.filter(profile=profile)

    context = {
        "notifications": notifications
    }

    return render(request, "notifications.html", context)


@login_required(redirect_field_name="log_in")
def check_notification(request, pk):

    notifications = Notification.objects.filter(pk=pk)
    if not notifications.exists():
        return redirect("feed")
    notification = notifications.first()
    notification.is_read = True

    notification.save()

    return redirect("post", notification.post.pk)


def check_all_notification(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    notifications = Notification.objects.filter(profile=profile)

    for notification in notifications:
        notification.is_read = True
        notification.save()

    return redirect("notification")


def notifications_button(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    
    has_notifications= Notification.objects.filter(profile=profile,is_read=True).exists()
    print(has_notifications)
    context={
        "has_notifications": has_notifications
    }
    
    return render(request, "htmx/notification_button.html", context)
